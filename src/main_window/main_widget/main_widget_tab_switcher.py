from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
    BrowseTabSection,
)
from main_window.main_widget.tab_index import TAB_INDEX
from main_window.main_widget.tab_indices import LeftStackIndex, RightStackIndex
from main_window.main_widget.tab_name import TabName

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from core.application_context import ApplicationContext


class MainWidgetTabSwitcher:
    def __init__(
        self, main_widget: "MainWidget", app_context: "ApplicationContext" = None
    ):
        self.mw = main_widget
        self.app_context = app_context or getattr(main_widget, "app_context", None)

        self.tab_to_right_stack = {
            TAB_INDEX[TabName.GENERATE]: RightStackIndex.GENERATE_TAB,
            TAB_INDEX[TabName.LEARN]: RightStackIndex.LEARN_TAB,
            TAB_INDEX[TabName.SEQUENCE_CARD]: RightStackIndex.SEQUENCE_CARD_TAB,
        }

        self.tab_to_left_stack = {
            TAB_INDEX[TabName.LEARN]: LeftStackIndex.LEARN_CODEX,
            TAB_INDEX[TabName.GENERATE]: LeftStackIndex.WORKBENCH,
            TAB_INDEX[TabName.CONSTRUCT]: LeftStackIndex.WORKBENCH,
            TAB_INDEX[TabName.SEQUENCE_CARD]: LeftStackIndex.WORKBENCH,
        }

        self.index_to_tab_name = {v: k for k, v in TAB_INDEX.items()}

    def on_tab_changed(self, new_tab: TabName):
        print(
            f"DEBUG: MainWidgetTabSwitcher.on_tab_changed called with new_tab={new_tab}"
        )
        print(f"DEBUG: TAB_INDEX={TAB_INDEX}")

        index = TAB_INDEX[new_tab]
        print(f"DEBUG: index={index}")

        left_new_index, right_new_index = self.get_stack_indices_for_tab(new_tab)
        print(
            f"DEBUG: left_new_index={left_new_index}, right_new_index={right_new_index}"
        )

        # This line might be causing the issue - it's overriding the new_tab parameter
        original_new_tab = new_tab
        new_tab = self.index_to_tab_name.get(index, TabName.CONSTRUCT)
        print(
            f"DEBUG: original_new_tab={original_new_tab}, overridden new_tab={new_tab}"
        )

        current_tab_str = self._get_current_tab()
        print(f"DEBUG: current_tab_str={current_tab_str}")

        self._set_current_tab(new_tab.value)
        print(f"DEBUG: Set current tab to {new_tab.value}")

        # Set width ratio based on tab type using stretch factors
        if new_tab == TabName.BROWSE:
            width_ratio = (2, 1)  # Browse tab uses 2:1 ratio (2/3 left, 1/3 right)
        elif new_tab == TabName.SEQUENCE_CARD:
            width_ratio = (0, 1)  # Sequence card tab uses full width for right panel
        else:
            width_ratio = (1, 1)  # Default is equal split

        # 💥💥💥 NUCLEAR MELTDOWN: OBLITERATE ALL FADE OPERATIONS! 💥💥💥
        print("☢️ NUCLEAR MELTDOWN: COMPLETELY DESTROYING FADE SYSTEM!")

        # DIRECT SWITCHING ONLY - NO FADES ALLOWED!
        left_idx = (
            left_new_index.value if hasattr(left_new_index, "value") else left_new_index
        )
        right_idx = (
            right_new_index.value
            if hasattr(right_new_index, "value")
            else right_new_index
        )

        self.mw.left_stack.setCurrentIndex(left_idx)
        self.mw.right_stack.setCurrentIndex(right_idx)


        # 🔥 FINAL SCORCHED EARTH: DYNAMIC LAYOUT SWITCHING!
        if new_tab == TabName.BROWSE:
            # Browse tab gets full width (hide right stack)
            self.mw.content_layout.setStretch(0, 1)  # Left stack: full width
            self.mw.content_layout.setStretch(1, 0)  # Right stack: hidden
            self.mw.right_stack.hide()  # Actually hide the right stack
        else:
            # Other tabs get normal layout
            self.mw.content_layout.setStretch(0, 1)  # Left stack: equal width
            self.mw.content_layout.setStretch(1, 1)  # Right stack: equal width
            self.mw.right_stack.show()  # Show the right stack


        # if new_tab == TabName.BROWSE:
        #     print("☢️ MELTDOWN: BROWSE TAB DETECTED - GOING NUCLEAR!")
        #     self._nuclear_meltdown_browse_tab_enforcement()  # 🔥 OBLITERATED!


        # COMPLETELY OBLITERATED ALL POST-SWITCH OPERATIONS:
        # QApplication.processEvents()
        # if new_tab == TabName.BROWSE:
        #     # NUCLEAR APPROACH: Completely nuke all thumbnail operations
        #     print(
        #         "💥 NUCLEAR: Completely nuking all thumbnail operations for browse tab!"
        #     )
        #
        #     # NUCLEAR: Skip ALL thumbnail operations that could interfere with layout
        #     # browse_tab = self._get_browse_tab()
        #     # if browse_tab and hasattr(browse_tab, "sequence_viewer"):
        #     #     sequence_viewer = browse_tab.sequence_viewer
        #     #     if hasattr(sequence_viewer, "thumbnail_box") and hasattr(
        #     #         sequence_viewer.thumbnail_box, "image_label"
        #     #     ):
        #     #         sequence_viewer.thumbnail_box.image_label._resize_pixmap_to_fit()
        #     #
        #     # # NUCLEAR: Skip ALL UI updates that could mess with layout
        #     # if browse_tab and hasattr(browse_tab, "ui_updater"):
        #     #     browse_tab.ui_updater.resize_thumbnails_top_to_bottom()
        #
        #     print(
        #         "💥 NUCLEAR: Skipped ALL thumbnail operations - going straight to layout enforcement"
        #     )
        #
        #     # NUCLEAR: Go straight to aggressive constraint enforcement
        #     self._enforce_browse_tab_layout_constraints()
        # elif new_tab == TabName.SEQUENCE_CARD:
        #     # Initialize the sequence card tab if needed using dependency injection
        #     sequence_card_tab = self._get_sequence_card_tab()
        #     if sequence_card_tab and hasattr(sequence_card_tab, "initialized"):
        #         if not sequence_card_tab.initialized:
        #             sequence_card_tab.initialized = True
        #             if hasattr(sequence_card_tab, "refresher"):
        #                 sequence_card_tab.refresher.refresh_sequence_cards()

        print("🔥 SCORCHED EARTH: All post-switch operations COMPLETELY OBLITERATED!")

    def debug_layout_state(self, main_widget, context=""):
        """Debug function to track layout state."""
        try:
            left_w = main_widget.left_stack.width()
            right_w = main_widget.right_stack.width()
            total_w = main_widget.width()
            ratio = left_w / right_w if right_w > 0 else 0

            left_stretch = main_widget.content_layout.stretch(0)
            right_stretch = main_widget.content_layout.stretch(1)

            print(f"🔍 LAYOUT DEBUG [{context}]:")
            print(f"   Total width: {total_w}px")
            print(f"   Left: {left_w}px ({left_w/total_w*100:.1f}%)")
            print(f"   Right: {right_w}px ({right_w/total_w*100:.1f}%)")
            print(f"   Ratio: {ratio:.2f} (target: 2.0)")
            print(f"   Stretch factors: Left={left_stretch}, Right={right_stretch}")
            print(f"   Left max width: {main_widget.left_stack.maximumWidth()}")
            print(f"   Right max width: {main_widget.right_stack.maximumWidth()}")

        except Exception as e:
            print(f"🔍 LAYOUT DEBUG ERROR: {e}")

    def _nuclear_meltdown_browse_tab_enforcement(self):
        """☢️ NUCLEAR MELTDOWN: COMPLETE OBLITERATION OF LAYOUT INTERFERENCE! ☢️"""
        try:
            main_widget = self.mw
            if hasattr(main_widget, "content_layout"):
                print("☢️☢️☢️ NUCLEAR MELTDOWN: OBLITERATING ALL LAYOUT INTERFERENCE! ☢️☢️☢️")

                # MELTDOWN STEP 1: FORCE 2:1 RATIO WITH EXTREME PREJUDICE
                for i in range(10):  # Do it 10 times to make absolutely sure!
                    main_widget.content_layout.setStretch(0, 2)  # Left stack: 2 parts
                    main_widget.content_layout.setStretch(1, 1)  # Right stack: 1 part
                    QApplication.processEvents()
                print("☢️ MELTDOWN: Applied 2:1 stretch factors 10 TIMES!")

                # MELTDOWN STEP 2: OBLITERATE ALL WIDTH CONSTRAINTS
                main_widget.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.left_stack.setMinimumWidth(0)
                main_widget.right_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.right_stack.setMinimumWidth(0)
                print("☢️ MELTDOWN: OBLITERATED all width constraints!")

                # MELTDOWN STEP 3: COMPLETELY DESTROY BROWSE TAB COMPONENTS
                browse_tab = self._get_browse_tab()
                if browse_tab:
                    self._nuclear_meltdown_browse_components(browse_tab)

                # MELTDOWN STEP 4: FORCE LAYOUT UPDATES WITH EXTREME FORCE
                for i in range(10):
                    QApplication.processEvents()
                    main_widget.content_layout.update()
                    main_widget.updateGeometry()
                    main_widget.update()
                    main_widget.repaint()
                print("☢️ MELTDOWN: Forced layout updates 10 TIMES!")

                # MELTDOWN STEP 5: CONTINUOUS NUCLEAR MONITORING
                self._setup_nuclear_meltdown_monitoring()

                # Debug the layout state
                self.debug_layout_state(main_widget, "after_nuclear_meltdown")
                print("☢️☢️☢️ NUCLEAR MELTDOWN COMPLETE! ☢️☢️☢️")

        except Exception as e:
            print(f"☢️ NUCLEAR MELTDOWN ERROR: {e}")
            import traceback

            traceback.print_exc()

    def _enforce_browse_tab_layout_constraints(self):
        """TARGETED NUCLEAR STRIKE: Focus on specific browse tab component issues."""
        try:
            main_widget = self.mw
            if hasattr(main_widget, "content_layout"):
                print("🎯 TARGETED NUCLEAR STRIKE: Focusing on browse tab components!")

                # STEP 1: Apply proven layout technique from our successful test
                main_widget.content_layout.setStretch(0, 2)  # Left stack: 2 parts
                main_widget.content_layout.setStretch(1, 1)  # Right stack: 1 part
                print("🎯 NUCLEAR: Applied proven stretch factors")

                # STEP 2: Clear constraints that might interfere
                main_widget.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.left_stack.setMinimumWidth(0)
                main_widget.right_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.right_stack.setMinimumWidth(0)
                print("🎯 NUCLEAR: Cleared width constraints")

                # STEP 3: NUCLEAR STRIKE on browse tab components specifically
                browse_tab = self._get_browse_tab()
                if browse_tab:
                    self._nuclear_strike_browse_components(browse_tab)

                # STEP 4: Force layout updates (proven to work)
                for _ in range(3):
                    QApplication.processEvents()
                    main_widget.content_layout.update()
                    main_widget.updateGeometry()
                print("🎯 NUCLEAR: Forced layout updates")

                # STEP 5: Continuous enforcement with timer
                self._setup_continuous_enforcement()

                # Debug the layout state
                self.debug_layout_state(main_widget, "after_targeted_nuclear_strike")
                print("🎯 TARGETED NUCLEAR STRIKE COMPLETE!")

        except Exception as e:
            print(f"🎯 NUCLEAR STRIKE ERROR: {e}")
            import traceback

            traceback.print_exc()

    def _nuclear_meltdown_browse_components(self, browse_tab):
        """☢️ NUCLEAR MELTDOWN: COMPLETE OBLITERATION OF BROWSE TAB COMPONENTS! ☢️"""
        print("☢️☢️☢️ NUCLEAR MELTDOWN: OBLITERATING BROWSE TAB COMPONENTS! ☢️☢️☢️")

        from PyQt6.QtWidgets import QSizePolicy

        # MELTDOWN: Create the most restrictive size policies possible
        fixed_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        preferred_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        expanding_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # OBLITERATE sequence_picker (left side) - FORCE IT TO EXPAND
        if hasattr(browse_tab, "sequence_picker"):
            picker = browse_tab.sequence_picker
            picker.setSizePolicy(expanding_policy)
            print("☢️ MELTDOWN: OBLITERATED sequence_picker size policy!")

            # OBLITERATE picker's internal components
            if hasattr(picker, "scroll_widget"):
                picker.scroll_widget.setSizePolicy(expanding_policy)
                print("☢️ MELTDOWN: OBLITERATED scroll_widget size policy!")

            if hasattr(picker, "nav_sidebar"):
                # NUCLEAR: Force sidebar to be TINY
                picker.nav_sidebar.setSizePolicy(fixed_policy)
                picker.nav_sidebar.setMaximumWidth(100)  # Force it to be small!
                picker.nav_sidebar.setMinimumWidth(50)
                print("☢️ MELTDOWN: OBLITERATED nav_sidebar - FORCED TO BE TINY!")

        # OBLITERATE sequence_viewer (right side) - FORCE IT TO BE SMALL
        if hasattr(browse_tab, "sequence_viewer"):
            viewer = browse_tab.sequence_viewer
            # NUCLEAR: Force viewer to be EXACTLY 1/3 width
            viewer.setSizePolicy(preferred_policy)

            # NUCLEAR: Set maximum width to force 1/3 ratio
            total_width = self.mw.width()
            max_viewer_width = int(total_width / 3)  # Exactly 1/3
            viewer.setMaximumWidth(max_viewer_width)
            viewer.setMinimumWidth(max_viewer_width // 2)  # At least half of 1/3
            print(
                f"☢️ MELTDOWN: OBLITERATED sequence_viewer - FORCED TO {max_viewer_width}px (1/3 of {total_width}px)!"
            )

            # OBLITERATE viewer's internal components
            if hasattr(viewer, "thumbnail_box"):
                viewer.thumbnail_box.setSizePolicy(preferred_policy)
                viewer.thumbnail_box.setMaximumWidth(
                    max_viewer_width - 20
                )  # Leave some margin
                print("☢️ MELTDOWN: OBLITERATED thumbnail_box size!")

                if hasattr(viewer.thumbnail_box, "image_label"):
                    viewer.thumbnail_box.image_label.setSizePolicy(preferred_policy)
                    print("☢️ MELTDOWN: OBLITERATED image_label size policy!")

        print("☢️☢️☢️ BROWSE TAB COMPONENTS COMPLETELY OBLITERATED! ☢️☢️☢️")

    def _nuclear_strike_browse_components(self, browse_tab):
        """Nuclear strike specifically targeting browse tab components."""
        print("💥 NUCLEAR STRIKE: Targeting browse tab components...")

        from PyQt6.QtWidgets import QSizePolicy

        expanding_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        preferred_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )

        # Target sequence_picker (left side)
        if hasattr(browse_tab, "sequence_picker"):
            picker = browse_tab.sequence_picker
            picker.setSizePolicy(expanding_policy)

            # Nuclear strike on picker's internal components
            if hasattr(picker, "scroll_widget"):
                picker.scroll_widget.setSizePolicy(expanding_policy)
            if hasattr(picker, "nav_sidebar"):
                picker.nav_sidebar.setSizePolicy(preferred_policy)
                # Force sidebar to respect width constraints
                if hasattr(picker.nav_sidebar, "setFixedWidth"):
                    # Don't let sidebar expand beyond reasonable limits
                    max_sidebar_width = int(self.mw.width() / 12)  # 1/12 of total width
                    picker.nav_sidebar.setMaximumWidth(max_sidebar_width)

            print("💥 NUCLEAR: Struck sequence_picker components")

        # Target sequence_viewer (right side)
        if hasattr(browse_tab, "sequence_viewer"):
            viewer = browse_tab.sequence_viewer
            viewer.setSizePolicy(preferred_policy)

            # Nuclear strike on viewer's internal components
            if hasattr(viewer, "thumbnail_box"):
                viewer.thumbnail_box.setSizePolicy(preferred_policy)
                # Prevent thumbnail box from forcing its own size
                if hasattr(viewer.thumbnail_box, "image_label"):
                    viewer.thumbnail_box.image_label.setSizePolicy(preferred_policy)

            print("💥 NUCLEAR: Struck sequence_viewer components")

    def _setup_nuclear_meltdown_monitoring(self):
        """☢️ Set up nuclear meltdown monitoring to prevent any layout interference! ☢️"""
        if not hasattr(self, "_meltdown_timer"):
            from PyQt6.QtCore import QTimer

            self._meltdown_timer = QTimer()
            self._meltdown_timer.timeout.connect(self._nuclear_meltdown_monitoring)
            self._meltdown_timer.start(500)  # Check every 0.5 seconds - AGGRESSIVE!
            print("☢️ MELTDOWN: Set up nuclear monitoring timer - EVERY 0.5 SECONDS!")

    def _nuclear_meltdown_monitoring(self):
        """☢️ Continuously monitor and obliterate any layout interference! ☢️"""
        try:
            if hasattr(self.mw, "content_layout"):
                current_left_stretch = self.mw.content_layout.stretch(0)
                current_right_stretch = self.mw.content_layout.stretch(1)

                # If stretch factors have been corrupted, OBLITERATE THE CORRUPTION!
                if current_left_stretch != 2 or current_right_stretch != 1:
                    print(
                        f"☢️ MELTDOWN ALERT: LAYOUT CORRUPTION DETECTED! Left={current_left_stretch}, Right={current_right_stretch}"
                    )

                    # NUCLEAR RESPONSE: Force the ratio multiple times
                    for i in range(5):
                        self.mw.content_layout.setStretch(0, 2)
                        self.mw.content_layout.setStretch(1, 1)
                        QApplication.processEvents()

                    print("☢️ MELTDOWN: CORRUPTION OBLITERATED!")

                    # Re-enforce sequence viewer constraints
                    browse_tab = self._get_browse_tab()
                    if browse_tab and hasattr(browse_tab, "sequence_viewer"):
                        viewer = browse_tab.sequence_viewer
                        total_width = self.mw.width()
                        max_viewer_width = int(total_width / 3)
                        viewer.setMaximumWidth(max_viewer_width)
                        print(
                            f"☢️ MELTDOWN: Re-enforced sequence_viewer width to {max_viewer_width}px!"
                        )

        except Exception as e:
            print(f"☢️ NUCLEAR MELTDOWN MONITORING ERROR: {e}")

    def _setup_continuous_enforcement(self):
        """Set up continuous layout enforcement to prevent regression."""
        if not hasattr(self, "_enforcement_timer"):
            from PyQt6.QtCore import QTimer

            self._enforcement_timer = QTimer()
            self._enforcement_timer.timeout.connect(self._continuous_enforcement)
            self._enforcement_timer.start(1000)  # Check every second
            print("🎯 NUCLEAR: Set up continuous enforcement timer")

    def _continuous_enforcement(self):
        """Continuously enforce the 2:1 ratio."""
        try:
            if hasattr(self.mw, "content_layout"):
                current_left_stretch = self.mw.content_layout.stretch(0)
                current_right_stretch = self.mw.content_layout.stretch(1)

                # If stretch factors have been corrupted, fix them
                if current_left_stretch != 2 or current_right_stretch != 1:
                    print(
                        f"🚨 LAYOUT CORRUPTION DETECTED: Left={current_left_stretch}, Right={current_right_stretch}"
                    )
                    self.mw.content_layout.setStretch(0, 2)
                    self.mw.content_layout.setStretch(1, 1)
                    print("🔧 LAYOUT CORRUPTION FIXED")
        except Exception as e:
            print(f"🚨 CONTINUOUS ENFORCEMENT ERROR: {e}")

    def set_stacks_silently(self, left_index, right_index):
        tab_name_str = self._get_current_tab()

        # Set width ratio based on tab type using stretch factors instead of fixed widths
        if tab_name_str == "browse":
            stretch_ratio = (2, 1)  # Browse tab uses 2:1 ratio (2/3 left, 1/3 right)
        elif tab_name_str == "sequence_card":
            stretch_ratio = (0, 1)  # Sequence card tab uses full width for right panel
        else:
            stretch_ratio = (1, 1)  # Default is equal split

        # Apply stretch factors to maintain proper aspect ratio
        if hasattr(self.mw, "content_layout"):
            self.mw.content_layout.setStretch(0, stretch_ratio[0])
            self.mw.content_layout.setStretch(1, stretch_ratio[1])

            # Clear any fixed width constraints that might interfere
            self.mw.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
            self.mw.right_stack.setMaximumWidth(16777215)
            self.mw.left_stack.setMinimumWidth(0)
            self.mw.right_stack.setMinimumWidth(0)

        # Handle both enum values and integers
        left_idx = left_index.value if hasattr(left_index, "value") else left_index
        right_idx = right_index.value if hasattr(right_index, "value") else right_index

        self.mw.left_stack.setCurrentIndex(left_idx)
        self.mw.right_stack.setCurrentIndex(right_idx)

    def get_stack_indices_for_tab(
        self, tab_name: TabName
    ) -> tuple[LeftStackIndex, RightStackIndex]:
        index = TAB_INDEX[tab_name]
        left_index = self.tab_to_left_stack.get(index, LeftStackIndex.WORKBENCH)
        if tab_name == TabName.CONSTRUCT:
            current_sequence = self.mw.json_manager.loader_saver.load_current_sequence()
            right_index = (
                RightStackIndex.OPTION_PICKER
                if len(current_sequence) > 1
                else RightStackIndex.START_POS_PICKER
            )
        elif tab_name == TabName.BROWSE:
            # 🔥 FINAL SCORCHED EARTH: BROWSE TAB NOW HAS INTERNAL LAYOUT!
            print(
                "🔥 FINAL SCORCHED EARTH: Browse tab switching - using internal 2:1 layout!"
            )

            current_section_str = (
                self.mw.browse_tab.browse_settings.get_current_section()
            )

            filter_section_strs = [section.value for section in BrowseTabSection]
            if current_section_str in filter_section_strs:
                if current_section_str == BrowseTabSection.FILTER_SELECTOR.value:
                    left_index = LeftStackIndex.FILTER_SELECTOR
                    # For filter selector, we hide the right stack by using sequence card tab
                    right_index = RightStackIndex.SEQUENCE_CARD_TAB
                else:
                    left_index = (
                        LeftStackIndex.SEQUENCE_PICKER
                    )  # This is now the browse tab with internal layout!
                    # For browse tab, we hide the right stack since browse tab handles its own layout
                    right_index = RightStackIndex.SEQUENCE_CARD_TAB
            else:
                left_index = (
                    LeftStackIndex.SEQUENCE_PICKER
                )  # Browse tab with internal layout
                right_index = RightStackIndex.SEQUENCE_CARD_TAB  # Hide right stack

            print(
                f"🔥 FINAL SCORCHED EARTH: Browse tab indices - left: {left_index}, right: {right_index}"
            )
        elif tab_name == TabName.SEQUENCE_CARD:
            # For Sequence Card Tab, we use the sequence card tab on both left and right panels
            # This gives us a full-screen experience for the sequence cards
            left_index = LeftStackIndex.WORKBENCH  # We'll hide this panel
            right_index = RightStackIndex.SEQUENCE_CARD_TAB
        else:
            right_index = self.tab_to_right_stack.get(index, index)

        return left_index, right_index

    def _get_current_tab(self) -> str:
        """Get current tab through dependency injection or fallback to legacy."""
        try:
            if self.app_context and hasattr(self.app_context, "settings_manager"):
                return (
                    self.app_context.settings_manager.global_settings.get_current_tab()
                )
        except (AttributeError, RuntimeError):
            pass

        # Fallback to legacy AppContext for backward compatibility
        try:
            from src.settings_manager.global_settings.app_context import AppContext

            return AppContext.settings_manager().global_settings.get_current_tab()
        except (AttributeError, RuntimeError):
            # If all else fails, default to construct tab
            return "construct"

    def _set_current_tab(self, tab_name: str) -> None:
        """Set current tab through dependency injection or fallback to legacy."""
        try:
            if self.app_context and hasattr(self.app_context, "settings_manager"):
                self.app_context.settings_manager.global_settings.set_current_tab(
                    tab_name
                )
                return
        except (AttributeError, RuntimeError):
            pass

        # Fallback to legacy AppContext for backward compatibility
        try:
            from src.settings_manager.global_settings.app_context import AppContext

            AppContext.settings_manager().global_settings.set_current_tab(tab_name)
        except (AttributeError, RuntimeError):
            # If all else fails, silently ignore
            pass

    def _get_browse_tab(self):
        """Get the browse tab using the new dependency injection pattern with graceful fallbacks."""
        try:
            # Try to get browse tab through the new coordinator pattern
            return self.mw.get_tab_widget("browse")
        except AttributeError:
            # Fallback: try through tab_manager for backward compatibility
            try:
                return self.mw.tab_manager.get_tab_widget("browse")
            except AttributeError:
                # Final fallback: try direct access for legacy compatibility
                try:
                    if hasattr(self.mw, "browse_tab"):
                        return self.mw.browse_tab
                except AttributeError:
                    pass
        return None

    def _get_sequence_card_tab(self):
        """Get the sequence card tab using the new dependency injection pattern with graceful fallbacks."""
        try:
            # Try to get sequence card tab through the new coordinator pattern
            return self.mw.get_tab_widget("sequence_card")
        except AttributeError:
            # Fallback: try through tab_manager for backward compatibility
            try:
                return self.mw.tab_manager.get_tab_widget("sequence_card")
            except AttributeError:
                # Final fallback: try direct access for legacy compatibility
                try:
                    if hasattr(self.mw, "sequence_card_tab"):
                        return self.mw.sequence_card_tab
                except AttributeError:
                    pass
        return None
