from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from .section_button import OptionPickerSectionButton
from .letter_types import LetterType


class OptionPickerSection(QWidget):
    def __init__(self, letter_type: str, parent=None, mw_size_provider=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.pictographs: List = []
        self.mw_size_provider = mw_size_provider  # V1-style size provider
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.header_button = OptionPickerSectionButton(self)
        self.header_button.clicked.connect(self._toggle_section)
        layout.addWidget(self.header_button)

        # V1-style container: simple QFrame with QGridLayout
        from PyQt6.QtWidgets import QFrame

        self.pictograph_container = QFrame()
        self.pictograph_layout = QGridLayout(self.pictograph_container)

        # V1-style layout settings
        self.pictograph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
        self.pictograph_layout.setSpacing(8)  # V1 uses spacing from option_scroll

        layout.addWidget(self.pictograph_container)

        # V1-style: transparent background, no borders
        self.pictograph_container.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                border: none;
            }
        """
        )

        # Initialize container visibility to match button state (expanded by default)
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def _toggle_section(self):
        self.header_button.toggle_expansion()
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def add_pictograph(self, pictograph_frame):
        """Add pictograph using V1-style direct layout positioning with lifecycle safety"""
        # Defensive check: ensure layout objects are still valid
        if not self._ensure_layout_validity():
            print(
                f"⚠️ Layout objects invalid, recreating for section {self.letter_type}"
            )
            self._recreate_layout_objects()
            # After recreation, check again
            if not self._ensure_layout_validity():
                print(
                    f"❌ Layout still invalid after recreation, cannot add pictograph"
                )
                return

        self.pictographs.append(pictograph_frame)

        # V1-style direct positioning: use COLUMN_COUNT = 8 and divmod calculation
        COLUMN_COUNT = 8  # V1's exact column count
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        try:
            # Double-check layout is still valid before adding widget
            if not self._ensure_layout_validity():
                print(f"❌ Layout became invalid during pictograph addition")
                # Remove from pictographs list since we can't add it
                self.pictographs.remove(pictograph_frame)
                return

            # Add directly to layout like V1 does
            self.pictograph_layout.addWidget(pictograph_frame, row, col)
            pictograph_frame.setVisible(True)

            print(
                f"🎯 V1-style add: pictograph {count} at ({row}, {col}) in section {self.letter_type}"
            )

            # Ensure container is large enough for V1-style 8-column layout
            # Do this after adding to avoid triggering deletion during resize
            self._update_container_size_for_v1_layout()

        except RuntimeError as e:
            print(f"❌ Qt object error in add_pictograph: {e}")
            # Remove from pictographs list since addition failed
            if pictograph_frame in self.pictographs:
                self.pictographs.remove(pictograph_frame)
            print(f"❌ Skipping pictograph addition to prevent widget deletion cascade")

    def clear_pictographs(self):
        """Clear pictographs using proper Qt widget lifecycle management"""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    # Cleanup resources first
                    if hasattr(pictograph, "cleanup"):
                        pictograph.cleanup()

                    # Remove from layout first
                    if self._ensure_layout_validity():
                        self.pictograph_layout.removeWidget(pictograph)

                    # Properly delete the widget to prevent Qt object lifecycle issues
                    pictograph.setParent(None)
                    pictograph.deleteLater()

                except RuntimeError as e:
                    print(f"⚠️ Qt object error in clear_pictographs: {e}")
                    # If widget is already deleted, just continue
                    pass

        self.pictographs.clear()
        print(f"🧹 V1-style clear: section {self.letter_type} cleared")

    def clear_pictographs_v1_style(self):
        """Clear pictographs using V1-style approach: hide and remove from layout, don't delete"""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    # V1-style: only remove from layout and hide, never delete
                    if self._ensure_layout_validity():
                        self.pictograph_layout.removeWidget(pictograph)
                    pictograph.setVisible(False)
                    # Don't call deleteLater() - this is the key difference from V2's original approach
                except RuntimeError as e:
                    print(f"⚠️ Qt object error in V1-style clear: {e}")
                    pass

        self.pictographs.clear()
        print(f"🧹 V1-style clear (no deletion): section {self.letter_type} cleared")

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph from pool using V1-style approach (reuse existing objects)"""
        # Defensive check: ensure layout objects are still valid
        if not self._ensure_layout_validity():
            print(
                f"⚠️ Layout objects invalid, recreating for section {self.letter_type}"
            )
            self._recreate_layout_objects()
            if not self._ensure_layout_validity():
                print(
                    f"❌ Layout still invalid after recreation, cannot add pictograph"
                )
                return

        self.pictographs.append(pictograph_frame)

        # V1-style direct positioning: use COLUMN_COUNT = 8 and divmod calculation
        COLUMN_COUNT = 8  # V1's exact column count
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        try:
            # Double-check layout is still valid before adding widget
            if not self._ensure_layout_validity():
                print(f"❌ Layout became invalid during pictograph addition")
                self.pictographs.remove(pictograph_frame)
                return

            # Add directly to layout like V1 does
            self.pictograph_layout.addWidget(pictograph_frame, row, col)

            # CRITICAL: Ensure pictograph is visible after adding to layout
            pictograph_frame.setVisible(True)
            pictograph_frame.show()  # Force show

            # Also ensure the pictograph component inside is visible
            if hasattr(pictograph_frame, "pictograph_component"):
                pictograph_frame.pictograph_component.setVisible(True)
                pictograph_frame.pictograph_component.show()

            print(
                f"🎯 V1-style pool reuse: pictograph {count} at ({row}, {col}) in section {self.letter_type}"
            )

            # CRITICAL: Force layout activation and geometry update
            self._force_layout_activation()

            # CRITICAL: Log actual pictograph positioning and dimensions
            self._log_pictograph_positioning(pictograph_frame, count, row, col)

            # Update container size after adding
            self._update_container_size_for_v1_layout()

        except RuntimeError as e:
            print(f"❌ Qt object error in add_pictograph_from_pool: {e}")
            if pictograph_frame in self.pictographs:
                self.pictographs.remove(pictograph_frame)
            print(
                f"❌ Skipping pool pictograph addition to prevent widget deletion cascade"
            )

    def _ensure_layout_validity(self) -> bool:
        """Check if layout objects are still valid (not deleted)"""
        try:
            # Try to access layout properties to check if they're still valid
            if self.pictograph_container is None:
                return False
            if self.pictograph_layout is None:
                return False

            # Try to access a property to see if the C++ object is still alive
            _ = self.pictograph_layout.count()
            _ = self.pictograph_container.isVisible()
            return True
        except (RuntimeError, AttributeError):
            return False

    def _recreate_layout_objects(self):
        """Recreate layout objects if they've been deleted"""
        try:
            print(f"🔧 Recreating layout objects for section {self.letter_type}")

            # Create new container and layout
            from PyQt6.QtWidgets import QFrame

            # Remove old container if it exists
            if (
                hasattr(self, "pictograph_container")
                and self.pictograph_container is not None
            ):
                try:
                    self.pictograph_container.setParent(None)
                except RuntimeError:
                    pass  # Already deleted

            # Create new container
            self.pictograph_container = QFrame()
            self.pictograph_layout = QGridLayout(self.pictograph_container)

            # V1-style layout settings
            self.pictograph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
            self.pictograph_layout.setSpacing(8)

            # Add to parent layout
            parent_layout = self.layout()
            if parent_layout:
                parent_layout.addWidget(self.pictograph_container)

            # Apply V1-style transparent styling
            self.pictograph_container.setStyleSheet(
                """
                QWidget {
                    background-color: transparent;
                    border: none;
                }
            """
            )

            # Set visibility
            self.pictograph_container.setVisible(self.header_button.is_expanded)

            print(f"✅ Layout objects recreated for section {self.letter_type}")

        except Exception as e:
            print(f"❌ Error recreating layout objects: {e}")

    def _update_container_size_for_v1_layout(self):
        """Update container size to accommodate V1-style 8-column layout with proper scroll area sizing"""
        if len(self.pictographs) == 0:
            return

        # Ensure container is still valid
        if not self._ensure_layout_validity():
            print(
                f"⚠️ Container invalid during sizing, recreating for section {self.letter_type}"
            )
            self._recreate_layout_objects()
            if not self._ensure_layout_validity():
                print(f"❌ Container still invalid after recreation, skipping sizing")
                return

        try:
            # V2-style sizing: different width handling for bottom row vs vertical sections
            if self.mw_size_provider:
                full_width = self.mw_size_provider().width()

                # Check if this section is in the bottom row (sections 4, 5, 6)
                if self.letter_type in [
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                ]:
                    # Bottom row sections share the width equally (1/3 each)
                    section_width = (full_width - 20) // 3  # Account for spacing
                    available_width = section_width - 20  # Account for margins
                    print(
                        f"🔧 V2-style sizing: Bottom row section {self.letter_type} gets {section_width}px (1/3 of {full_width}px), available {available_width}"
                    )
                else:
                    # Vertical sections (1, 2, 3) get full width
                    section_width = full_width
                    available_width = section_width - 40  # Account for margins
                    print(
                        f"🔧 V2-style sizing: Vertical section {self.letter_type} gets full width {section_width}px, available {available_width}"
                    )
            else:
                # Fallback to old method if no size provider
                available_width = self._get_available_scroll_width()
                print(f"🔧 Fallback sizing: Using scroll area width {available_width}")

            # V1-style responsive sizing: calculate optimal pictograph size
            # Adjust column count based on section type and available width
            if self.letter_type in [
                LetterType.TYPE4,
                LetterType.TYPE5,
                LetterType.TYPE6,
            ]:
                # Bottom row sections have less width, so fewer columns
                COLUMN_COUNT = min(
                    4, max(2, available_width // 80)
                )  # Adaptive based on width
            else:
                # Vertical sections can have more columns
                COLUMN_COUNT = 8

            container_margins = 10  # Reduced from 20
            grid_spacing = 8

            # Calculate pictograph size based on available width
            total_spacing = grid_spacing * (COLUMN_COUNT - 1)
            available_for_pictographs = (
                available_width - (2 * container_margins) - total_spacing
            )
            pictograph_size = max(
                60, min(160, available_for_pictographs // COLUMN_COUNT)
            )

            print(
                f"🔧 Section {self.letter_type}: Using {COLUMN_COUNT} columns, pictograph size {pictograph_size}px"
            )

            # CRITICAL FIX: Resize pictograph frames FIRST, before calculating container size
            # This ensures the QGridLayout calculations are based on the correct frame sizes
            self._resize_pictograph_frames(pictograph_size)

            # V1-style container sizing: use full available width
            actual_width = available_width  # Use full available width like V1

            # Calculate required dimensions
            max_row = (len(self.pictographs) - 1) // COLUMN_COUNT
            rows_needed = max_row + 1

            container_height = (
                (rows_needed * pictograph_size)
                + (grid_spacing * (rows_needed - 1))
                + (2 * container_margins)
            )

            # Double-check container is still valid before setting size
            if not self._ensure_layout_validity():
                print(f"❌ Container became invalid during sizing calculation")
                return

            # Apply responsive sizing to pictograph container
            # CRITICAL FIX: Don't set fixed height - let QGridLayout manage height naturally
            self.pictograph_container.setMinimumSize(actual_width, container_height)
            self.pictograph_container.setMaximumWidth(actual_width)  # Prevent overflow
            # REMOVED: setFixedHeight() - this was constraining the layout too much

            # Set size policy for proper scroll area behavior
            from PyQt6.QtWidgets import QSizePolicy

            self.pictograph_container.setSizePolicy(
                QSizePolicy.Policy.Preferred,  # Don't expand beyond needed width
                QSizePolicy.Policy.Minimum,  # Allow height to expand as needed by QGridLayout
            )

            # Update section sizing to fit content properly
            section_height = container_height + 60  # Space for header
            self.setMinimumHeight(section_height)
            # REMOVED: setMaximumHeight() - let section expand as needed
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,  # Allow height to expand as needed
            )

            print(
                f"🔧 Responsive container sizing: {actual_width}x{container_height} for {rows_needed} rows x {COLUMN_COUNT} cols"
            )
            print(
                f"🔧 Pictograph size: {pictograph_size}px (available width: {available_width}px)"
            )

            # Force layout to recalculate with new frame sizes
            self._force_layout_activation()

            # CRITICAL: Ensure container and section are visible
            self.pictograph_container.setVisible(True)
            self.pictograph_container.show()
            self.setVisible(True)
            self.show()

        except RuntimeError as e:
            print(f"❌ Qt object error in container sizing: {e}")
            print(f"❌ Skipping container sizing to prevent widget deletion cascade")

    def _get_available_scroll_width(self) -> int:
        """Get available width from parent scroll area, accounting for scroll bars"""
        # Default fallback width
        default_width = 600

        # Try to find the scroll area in parent hierarchy
        parent = self.parent()
        while parent:
            if hasattr(parent, "viewport") and hasattr(parent, "verticalScrollBar"):
                # Found scroll area
                viewport_width = parent.viewport().width()
                scrollbar_width = (
                    parent.verticalScrollBar().width()
                    if parent.verticalScrollBar().isVisible()
                    else 0
                )
                available_width = (
                    viewport_width - scrollbar_width - 20
                )  # Account for margins
                print(
                    f"🔧 Found scroll area: viewport={viewport_width}, scrollbar={scrollbar_width}, available={available_width}"
                )
                return max(400, available_width)  # Minimum reasonable width
            parent = parent.parent()

        print(f"🔧 No scroll area found, using default width: {default_width}")
        return default_width

    def _resize_pictograph_frames(self, target_size: int) -> None:
        """Resize all pictograph frames to the target size"""
        for pictograph_frame in self.pictographs:
            if pictograph_frame and hasattr(pictograph_frame, "setFixedSize"):
                try:
                    pictograph_frame.setFixedSize(target_size, target_size)
                    print(f"🔧 Resized pictograph frame to {target_size}x{target_size}")
                except RuntimeError:
                    # Frame may have been deleted
                    continue

    def _force_layout_activation(self) -> None:
        """Force the QGridLayout to activate and position widgets correctly"""
        try:
            # Force layout to calculate positions
            self.pictograph_layout.activate()
            self.pictograph_layout.update()

            # Force container to update its geometry
            self.pictograph_container.updateGeometry()

            # Process any pending layout events
            from PyQt6.QtWidgets import QApplication

            QApplication.processEvents()

            print(f"🔧 Forced layout activation for {self.letter_type}")

        except RuntimeError as e:
            print(f"❌ Error forcing layout activation: {e}")

    def update_layout(self):
        # DISABLED: This method was causing infinite loops and 2-pixel-high containers
        # V1-style sizing is handled in _update_container_size_for_v1_layout() instead
        print(
            f"🔧 update_layout() disabled for {self.letter_type} to prevent infinite loops"
        )
        return

    def _calculate_optimal_columns(self) -> int:
        """Calculate optimal columns based on V1 behavior and available width"""
        # Get available width from the option picker container
        available_width = 600  # Default fallback

        # Try to get actual available width from parent hierarchy
        parent = self.parent()
        while parent:
            if hasattr(parent, "sections_container"):
                available_width = (
                    parent.sections_container.width() - 40
                )  # Account for margins
                break
            parent = parent.parent()

        pictograph_width = 160 + 8  # Frame width + spacing

        # Calculate max columns that fit
        max_possible_columns = max(1, available_width // pictograph_width)

        # Apply V1-style limits based on letter type (but more generous than before)
        if self.letter_type == LetterType.TYPE1:
            # Type1 can have more columns like V1's COLUMN_COUNT = 8
            max_columns = min(8, max_possible_columns)
        elif self.letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            max_columns = min(6, max_possible_columns)
        else:
            max_columns = min(7, max_possible_columns)

        result = max(2, max_columns)
        print(
            f"🔧 Column calculation for {self.letter_type}: available_width={available_width}, max_possible={max_possible_columns}, result={result}"
        )
        return result

    def _log_pictograph_positioning(self, pictograph_frame, count, row, col):
        """Log comprehensive positioning information for each pictograph"""
        try:
            # Get pictograph frame dimensions and position
            frame_size = pictograph_frame.size()
            frame_pos = pictograph_frame.pos()
            frame_geometry = pictograph_frame.geometry()

            # Get global position (position in window)
            global_pos = pictograph_frame.mapToGlobal(pictograph_frame.rect().topLeft())

            # Get position relative to section
            section_pos = pictograph_frame.mapTo(
                self, pictograph_frame.rect().topLeft()
            )

            # Get position relative to container
            container_pos = pictograph_frame.mapTo(
                self.pictograph_container, pictograph_frame.rect().topLeft()
            )

            print(f"📍 PICTOGRAPH {count} POSITIONING ANALYSIS:")
            print(f"   Grid Position: ({row}, {col})")
            print(f"   Frame Size: {frame_size.width()}x{frame_size.height()}")
            print(
                f"   Frame Pos (relative to parent): ({frame_pos.x()}, {frame_pos.y()})"
            )
            print(
                f"   Frame Geometry: x={frame_geometry.x()}, y={frame_geometry.y()}, w={frame_geometry.width()}, h={frame_geometry.height()}"
            )
            print(
                f"   Global Position (window coords): ({global_pos.x()}, {global_pos.y()})"
            )
            print(
                f"   Position relative to section: ({section_pos.x()}, {section_pos.y()})"
            )
            print(
                f"   Position relative to container: ({container_pos.x()}, {container_pos.y()})"
            )
            print(f"   Visible: {pictograph_frame.isVisible()}")
            print(
                f"   Parent: {type(pictograph_frame.parent()).__name__ if pictograph_frame.parent() else 'None'}"
            )

            # Check if pictographs are overlapping by comparing positions
            if count > 1:
                # Compare with previous pictograph positions
                for i, other_frame in enumerate(
                    self.pictographs[:-1]
                ):  # Exclude current one
                    try:
                        other_pos = other_frame.pos()
                        other_global = other_frame.mapToGlobal(
                            other_frame.rect().topLeft()
                        )

                        # Check for overlap
                        if (
                            abs(frame_pos.x() - other_pos.x()) < 10
                            and abs(frame_pos.y() - other_pos.y()) < 10
                        ):
                            print(f"   ⚠️ OVERLAP DETECTED with pictograph {i+1}!")
                            print(
                                f"      This: ({frame_pos.x()}, {frame_pos.y()}) vs Other: ({other_pos.x()}, {other_pos.y()})"
                            )

                        if (
                            abs(global_pos.x() - other_global.x()) < 10
                            and abs(global_pos.y() - other_global.y()) < 10
                        ):
                            print(f"   🚨 GLOBAL OVERLAP with pictograph {i+1}!")
                            print(
                                f"      This global: ({global_pos.x()}, {global_pos.y()}) vs Other global: ({other_global.x()}, {other_global.y()})"
                            )
                    except RuntimeError:
                        # Other frame deleted, skip
                        continue

        except Exception as e:
            print(f"❌ Error logging pictograph positioning: {e}")

    def resizeEvent(self, event):
        """V2-style resize event to set proper section width"""
        if self.mw_size_provider:
            # V2 pattern: different width handling for bottom row vs vertical sections
            full_width = self.mw_size_provider().width()

            # Check if this section is in the bottom row (sections 4, 5, 6)
            if self.letter_type in [
                LetterType.TYPE4,
                LetterType.TYPE5,
                LetterType.TYPE6,
            ]:
                # Bottom row sections share the width equally (1/3 each)
                section_width = (
                    full_width - 20
                ) // 3  # Account for spacing between sections
                print(
                    f"🔧 V2-style resize: Setting bottom row section {self.letter_type} width to {section_width}px (1/3 of {full_width}px)"
                )
            else:
                # Vertical sections (1, 2, 3) get full width
                section_width = full_width
                print(
                    f"🔧 V2-style resize: Setting vertical section {self.letter_type} width to {section_width}px"
                )

            # Set the calculated width
            self.setFixedWidth(section_width)

            # Also ensure pictograph container uses available width
            if hasattr(self, "pictograph_container") and self.pictograph_container:
                container_width = section_width - 20  # Account for margins
                self.pictograph_container.setMinimumWidth(container_width)
                self.pictograph_container.setMaximumWidth(container_width)

                print(
                    f"🔧 V2-style resize: Setting container width to {container_width}px"
                )

        super().resizeEvent(event)
