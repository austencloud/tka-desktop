from typing import TYPE_CHECKING
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerGoBackButton(StyledButton):
    """A go-back button that returns to the initial filter selection."""

    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__("Go Back")
        self.sequence_picker = sequence_picker
        self.browse_tab = self.sequence_picker.browse_tab
        self.main_widget = self.sequence_picker.main_widget

        # Debug widget hierarchy and properties
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Creating go back button - parent: {sequence_picker}")
        logger.info(f"Button parent hierarchy: {self.parent()}")

        # Make sure the connection is properly established
        self.clicked.connect(self.switch_to_initial_filter_selection)
        logger.info(
            "Button clicked signal connected to switch_to_initial_filter_selection"
        )

        # Debug: Ensure the button is enabled and clickable
        self.setEnabled(True)
        self.setVisible(True)
        self.show()

        # Force focus policy to ensure it can receive events
        from PyQt6.QtCore import Qt

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Debug final state
        logger.info(
            f"Button initialized - enabled: {self.isEnabled()}, visible: {self.isVisible()}"
        )
        logger.info(f"Button size: {self.size()}, position: {self.pos()}")
        logger.info(
            f"Button accepts mouse events: {self.testAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)}"
        )

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the browse tab's internal filter stack."""
        import logging

        logger = logging.getLogger(__name__)

        try:
            logger.info("🔥 GO BACK BUTTON CLICKED - SIGNAL RECEIVED!")
            logger.info(
                "Go back button clicked - starting navigation to filter selector"
            )

            # Debug widget hierarchy and state
            logger.info(f"Button parent: {self.parent()}")
            logger.info(f"Sequence picker: {self.sequence_picker}")
            logger.info(f"Browse tab: {self.browse_tab}")
            logger.info(f"Main widget: {self.main_widget}")

            # Get the filter stack and debug its state
            filter_stack = self.sequence_picker.filter_stack
            logger.info(f"Filter stack: {filter_stack}")
            logger.info(f"Filter stack type: {type(filter_stack)}")
            logger.info(f"Filter stack current index: {filter_stack.currentIndex()}")
            logger.info(f"Filter stack widget count: {filter_stack.count()}")

            # Get the index of the filter selector (should be 0)
            from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
                BrowseTabSection,
            )

            logger.info(f"Available BrowseTabSection values: {list(BrowseTabSection)}")
            logger.info(f"Filter stack section_indexes: {filter_stack.section_indexes}")

            filter_selector_index = filter_stack.section_indexes.get(
                BrowseTabSection.FILTER_SELECTOR, 0
            )

            logger.info(
                f"Filter selector index: {filter_selector_index}, Available sections: {list(filter_stack.section_indexes.keys())}"
            )

            # Debug fade manager availability
            logger.info(
                f"Main widget has fade_manager: {hasattr(self.main_widget, 'fade_manager')}"
            )
            if hasattr(self.main_widget, "fade_manager"):
                logger.info(f"Fade manager: {self.main_widget.fade_manager}")
                logger.info(
                    f"Fade manager has stack_fader: {hasattr(self.main_widget.fade_manager, 'stack_fader')}"
                )
                if hasattr(self.main_widget.fade_manager, "stack_fader"):
                    logger.info(
                        f"Stack fader: {self.main_widget.fade_manager.stack_fader}"
                    )
                    logger.info(
                        f"Stack fader is not None: {self.main_widget.fade_manager.stack_fader is not None}"
                    )

            # ARCHITECTURAL FIX: Switch the browse tab's internal stack to show the filter stack
            # This is the correct approach - manipulate the stack that the button actually lives in
            logger.info("🔄 Switching browse tab internal stack to filter stack...")

            if hasattr(self.browse_tab, "internal_left_stack"):
                internal_stack = self.browse_tab.internal_left_stack
                filter_stack_index = 0  # Filter stack is at index 0 in internal stack

                logger.info(
                    f"Internal stack current index: {internal_stack.currentIndex()}"
                )
                logger.info(f"Switching to filter stack index: {filter_stack_index}")

                # Switch to filter stack in browse tab's internal stack
                internal_stack.setCurrentIndex(filter_stack_index)
                logger.info(f"✅ Internal stack switched to index {filter_stack_index}")

                # Now switch the filter stack to the filter selector
                logger.info("🔄 Switching filter stack to filter selector...")
                filter_stack = self.sequence_picker.filter_stack

                from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
                    BrowseTabSection,
                )

                filter_selector_index = filter_stack.section_indexes.get(
                    BrowseTabSection.FILTER_SELECTOR, 0
                )

                logger.info(f"Filter selector index: {filter_selector_index}")
                filter_stack.setCurrentIndex(filter_selector_index)
                logger.info(f"✅ Filter stack switched to filter selector")

            else:
                logger.error("❌ Browse tab has no internal_left_stack attribute")
                # Fallback: try the old method
                logger.info("🔄 Falling back to filter stack manipulation only...")
                filter_stack = self.sequence_picker.filter_stack

            # Test if the index is valid
            if filter_selector_index < filter_stack.count():
                logger.info(
                    f"✅ Index {filter_selector_index} is valid (stack has {filter_stack.count()} widgets)"
                )
                filter_stack.setCurrentIndex(filter_selector_index)
                logger.info(
                    f"✅ setCurrentIndex called - new current index: {filter_stack.currentIndex()}"
                )
            else:
                logger.error(
                    f"❌ Index {filter_selector_index} is invalid (stack has {filter_stack.count()} widgets)"
                )
                # Try index 0 as fallback
                logger.info("🔄 Trying index 0 as fallback")
                filter_stack.setCurrentIndex(0)
                logger.info(
                    f"✅ Fallback setCurrentIndex(0) called - new current index: {filter_stack.currentIndex()}"
                )

            # Update browse tab state to reflect the change
            # FIX: Use proper empty dict instead of None for current_filter
            self.browse_tab.browse_settings.set_current_section("filter_selector")
            self.browse_tab.browse_settings.set_current_filter(
                {}
            )  # Use empty dict instead of None

            # Update the filter stack's current section tracking
            filter_stack.current_filter_section = BrowseTabSection.FILTER_SELECTOR

            # Additional fix: Also update the browse tab state object if it exists
            if hasattr(self.browse_tab, "state") and self.browse_tab.state:
                self.browse_tab.state.set_current_section("filter_selector")
                self.browse_tab.state.set_current_filter(
                    ""
                )  # Use empty string for state

            logger.info("Successfully switched to filter selector")

        except Exception as e:
            logger.error(f"Failed to switch to initial filter selection: {e}")
            import traceback

            traceback.print_exc()

            # Emergency fallback: try direct index switching
            try:
                logger.info("Attempting emergency fallback...")
                self.sequence_picker.filter_stack.setCurrentIndex(0)
                self.browse_tab.browse_settings.set_current_section("filter_selector")
                self.browse_tab.browse_settings.set_current_filter(
                    {}
                )  # Fix: Use empty dict

                # Also update state in fallback
                if hasattr(self.browse_tab, "state") and self.browse_tab.state:
                    self.browse_tab.state.set_current_section("filter_selector")
                    self.browse_tab.state.set_current_filter("")

                logger.info("Emergency fallback succeeded")
            except Exception as fallback_error:
                logger.error(f"Emergency fallback also failed: {fallback_error}")

    def mousePressEvent(self, event):
        """Override mouse press event to ensure click is registered."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🖱️ MOUSE PRESS EVENT TRIGGERED!")
        logger.info(
            f"Go back button mouse press detected - button enabled: {self.isEnabled()}, visible: {self.isVisible()}"
        )
        logger.info(f"Mouse event position: {event.pos()}")
        logger.info(f"Mouse event button: {event.button()}")
        logger.info(f"Widget geometry: {self.geometry()}")
        logger.info(f"Widget rect: {self.rect()}")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Override mouse release event to ensure click is registered."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🖱️ MOUSE RELEASE EVENT TRIGGERED!")
        logger.info(
            f"Go back button mouse release detected - button enabled: {self.isEnabled()}, visible: {self.isVisible()}"
        )
        logger.info(f"Mouse event position: {event.pos()}")
        logger.info(f"Mouse event button: {event.button()}")
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """Override enter event to debug mouse tracking."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🖱️ MOUSE ENTERED BUTTON AREA!")
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Override leave event to debug mouse tracking."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🖱️ MOUSE LEFT BUTTON AREA!")
        super().leaveEvent(event)

    def event(self, event):
        """Override general event handler to catch all events."""
        import logging
        from PyQt6.QtCore import QEvent

        logger = logging.getLogger(__name__)

        # Log important events
        if event.type() in [
            QEvent.Type.MouseButtonPress,
            QEvent.Type.MouseButtonRelease,
            QEvent.Type.MouseMove,
            QEvent.Type.Enter,
            QEvent.Type.Leave,
        ]:
            logger.info(f"🎯 EVENT: {event.type()} on go back button")

        return super().event(event)

    def test_button_functionality(self):
        """Test method to verify button functionality programmatically."""
        import logging

        logger = logging.getLogger(__name__)

        logger.info("🧪 TESTING BUTTON FUNCTIONALITY PROGRAMMATICALLY")
        logger.info(f"Button enabled: {self.isEnabled()}")
        logger.info(f"Button visible: {self.isVisible()}")
        logger.info(f"Button size: {self.size()}")
        logger.info(f"Button position: {self.pos()}")
        logger.info(f"Button parent: {self.parent()}")

        # Test signal emission
        logger.info("🔄 Emitting clicked signal manually...")
        self.clicked.emit()
        logger.info("✅ Clicked signal emitted")

        # Test direct method call
        logger.info("🔄 Calling switch_to_initial_filter_selection directly...")
        self.switch_to_initial_filter_selection()
        logger.info("✅ Direct method call completed")

    def resizeEvent(self, event) -> None:
        """Handle resizing to update styles dynamically."""
        # GO BACK BUTTON SIZING FIX: Add proper initialization checks
        try:
            # Check if sequence picker is properly initialized
            if not self.sequence_picker:
                # Defer sizing until sequence picker is available
                from PyQt6.QtCore import QTimer

                QTimer.singleShot(100, lambda: self.resizeEvent(event))
                return

            # Get parent dimensions with validation
            parent_width = self.sequence_picker.width()
            parent_height = self.sequence_picker.height()

            # Check if parent has valid dimensions
            if parent_width <= 0 or parent_height <= 0:
                # Parent not fully initialized yet, defer sizing
                from PyQt6.QtCore import QTimer

                QTimer.singleShot(100, lambda: self.resizeEvent(event))
                return

            # Additional check: ensure browse tab is properly sized
            if hasattr(self, "browse_tab") and self.browse_tab:
                browse_tab_width = self.browse_tab.width()
                if browse_tab_width <= 0:
                    # Browse tab not ready, defer sizing
                    from PyQt6.QtCore import QTimer

                    QTimer.singleShot(100, lambda: self.resizeEvent(event))
                    return

            # Set button size to be more reasonable - larger than before
            button_width = max(
                80, parent_width // 8
            )  # Minimum 80px, or 1/8 of parent width
            button_height = max(
                30, parent_height // 20
            )  # Minimum 30px, or 1/20 of parent height

            self.setFixedWidth(button_width)
            self.setFixedHeight(button_height)

            # Update border radius after setting size
            self._border_radius = min(self.height(), self.width()) // 4  # Less rounded

            # Set reasonable font size based on button height
            font = self.font()
            font_size = max(
                8, min(16, button_height // 2)
            )  # Between 8-16pt, based on button height
            font.setPointSize(font_size)
            self.setFont(font)

            # Update appearance after all size changes
            self.update_appearance()

        except Exception as e:
            # Fallback to default size if calculation fails
            self.setFixedSize(80, 30)
            font = self.font()
            font.setPointSize(10)
            self.setFont(font)
            self._border_radius = 7  # Default border radius
            self.update_appearance()

            # Try again later in case it was a temporary issue
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(200, lambda: self.resizeEvent(event))

        super().resizeEvent(event)
