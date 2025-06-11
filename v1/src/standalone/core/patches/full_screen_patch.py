#!/usr/bin/env python3
"""
Patch for the full screen viewer to work properly in standalone environment.
This monkey patches the FullScreenViewer to use our custom overlay.
"""


def patch_full_screen_viewer_for_standalone():
    """Patch the FullScreenViewer to work in standalone environment."""

    try:
        from main_window.main_widget.sequence_workbench.full_screen_viewer import (
            FullScreenViewer,
        )
        from main_window.main_widget.full_screen_image_overlay import (
            FullScreenImageOverlay,
        )
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtWidgets import QApplication, QMessageBox

        # Store the original view_full_screen method
        original_view_full_screen = FullScreenViewer.view_full_screen

        def standalone_view_full_screen(self):
            """Modified view_full_screen method for standalone environment."""
            mw = self.main_widget
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

            # Get sequence length from UI state instead of JSON to ensure accuracy
            current_sequence = self._get_current_sequence_from_ui()
            sequence_length = len(current_sequence)

            if sequence_length <= 1:  # Changed from <= 2 to <= 1 to be less restrictive
                self.indicator_label.show_message("Please build a sequence first.")
                QApplication.restoreOverrideCursor()
                return
            else:
                # Use standalone image creator for better results
                current_thumbnail = self._create_standalone_thumbnail(current_sequence)
                if current_thumbnail:
                    pixmap = QPixmap(current_thumbnail)

                    # Check if we're in standalone environment
                    if hasattr(mw, "_create_full_screen_overlay"):
                        # Use standalone overlay
                        print(f"🎯 Creating standalone overlay...")
                        print(f"   mw type: {type(mw).__name__}")
                        print(
                            f"   mw.main_window type: {type(mw.main_window).__name__}"
                        )
                        overlay_class = mw._create_full_screen_overlay(mw)
                        print(f"   overlay_class: {overlay_class}")
                        full_screen_overlay = overlay_class(mw.main_window)
                        print(
                            f"   overlay instance: {type(full_screen_overlay).__name__}"
                        )
                    else:
                        # Use regular overlay for main application
                        full_screen_overlay = None
                        try:
                            # Try to get existing overlay using widget manager
                            if hasattr(mw, "get_widget"):
                                full_screen_overlay = mw.get_widget(
                                    "full_screen_overlay"
                                )
                        except (AttributeError, KeyError):
                            # Widget manager not available or overlay not found
                            pass

                        if not full_screen_overlay:
                            # Create overlay if it doesn't exist
                            full_screen_overlay = FullScreenImageOverlay(mw)
                            # Store it for future use if the widget manager supports it
                            try:
                                if hasattr(mw, "widget_manager") and hasattr(
                                    mw.widget_manager, "_widgets"
                                ):
                                    mw.widget_manager._widgets[
                                        "full_screen_overlay"
                                    ] = full_screen_overlay
                            except (AttributeError, TypeError):
                                # Widget manager not available - overlay will still work
                                pass

                    print(f"🖼️  Showing overlay...")
                    print(f"   pixmap size: {pixmap.width()}x{pixmap.height()}")
                    print(f"   pixmap null: {pixmap.isNull()}")
                    full_screen_overlay.show(pixmap)
                    print(
                        f"   overlay visible after show(): {full_screen_overlay.isVisible()}"
                    )
                    print(f"   overlay geometry: {full_screen_overlay.geometry()}")
                    print(
                        f"   overlay window flags: {full_screen_overlay.windowFlags()}"
                    )
                    QApplication.restoreOverrideCursor()
                else:
                    QMessageBox.warning(
                        None, "No Image", "Please select an image first."
                    )
                    QApplication.restoreOverrideCursor()

        def _create_standalone_thumbnail(self, sequence_data):
            """Create thumbnail using standalone image creator."""
            try:
                from standalone.services.image_creator.image_creator import (
                    StandaloneImageCreator,
                )

                print(f"🎨 Creating thumbnail with standalone image creator...")
                print(f"   Sequence data length: {len(sequence_data)}")

                # Create standalone image creator
                image_creator = StandaloneImageCreator()

                # Create options for full screen preview
                options = {
                    "include_start_position": True,
                    "add_user_info": False,  # Disable for full screen
                    "add_word": False,  # Disable for full screen
                    "add_difficulty_level": False,  # Disable for full screen
                    "add_beat_numbers": True,
                    "add_reversal_symbols": True,
                    "combined_grids": False,
                }

                # Create the image
                qimage = image_creator.create_sequence_image(
                    sequence_data=sequence_data,
                    options=options,
                    user_name="User",
                    export_date="",
                )

                if qimage and not qimage.isNull():
                    print(
                        f"✅ Standalone thumbnail created: {qimage.width()}x{qimage.height()}"
                    )

                    # Save to temporary file and return path
                    import tempfile
                    import os

                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, "standalone_thumbnail.png")

                    if qimage.save(temp_path, "PNG"):
                        print(f"✅ Thumbnail saved to: {temp_path}")
                        return temp_path
                    else:
                        print("❌ Failed to save thumbnail")
                        return None
                else:
                    print("❌ Failed to create thumbnail image")
                    return None

            except Exception as e:
                print(f"❌ Standalone thumbnail creation failed: {e}")
                import traceback

                traceback.print_exc()
                return None

        # Add the method to the FullScreenViewer class
        FullScreenViewer._create_standalone_thumbnail = _create_standalone_thumbnail

        # Replace the method
        FullScreenViewer.view_full_screen = standalone_view_full_screen

        print("✅ Full screen viewer patched for standalone environment")
        return True

    except Exception as e:
        print(f"⚠️  Could not patch full screen viewer: {e}")
        return False


if __name__ == "__main__":
    # Test the patch
    success = patch_full_screen_viewer_for_standalone()
    if success:
        print("Full screen viewer patch applied successfully!")
    else:
        print("Failed to apply full screen viewer patch")
