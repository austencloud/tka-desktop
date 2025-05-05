from typing import TYPE_CHECKING, Dict, List, Set, Tuple
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QGridLayout,
    QFileDialog,
    QMessageBox,
    QProgressDialog,
    QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter

from base_widgets.pictograph.pictograph import Pictograph
from data.constants import (
    GRID_MODE,
    RED,
    BLUE,
)
from enums.letter.letter import Letter
from main_window.main_widget.grid_mode_checker import GridModeChecker
from main_window.main_widget.settings_dialog.ui.image_export.fixed_codex_pictograph_exporter import (
    FixedCodexPictographExporter,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class CodexPictographExporterDialog(QDialog):
    """
    Dialog for configuring and exporting pictographs with specific turns applied.
    """

    def __init__(self, image_export_tab: "ImageExportTab"):
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        self.codex_exporter = FixedCodexPictographExporter(image_export_tab)

        # Track which pictograph types to export
        self.pictograph_types_to_export = {
            "A": True,
            "B": True,
            "C": True,
            "D": True,
            "E": True,
            "F": True,
        }

        # Initialize UI
        self.setWindowTitle("Export Pictographs with Turns")
        self.resize(500, 400)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the dialog UI components."""
        main_layout = QVBoxLayout(self)

        # Pictograph selection group
        pictograph_group = QGroupBox("Select Pictograph Types to Export")
        pictograph_layout = QGridLayout()

        # Create checkboxes for each pictograph type
        self.pictograph_checkboxes = {}
        row, col = 0, 0
        for letter in "ABCDEF":
            checkbox = QCheckBox(letter)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                lambda state, letter=letter: self._on_pictograph_checkbox_changed(
                    state, letter
                )
            )
            self.pictograph_checkboxes[letter] = checkbox
            pictograph_layout.addWidget(checkbox, row, col)
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1

        pictograph_group.setLayout(pictograph_layout)
        main_layout.addWidget(pictograph_group)

        # Turn configuration group
        turn_group = QGroupBox("Turn Configuration")
        turn_layout = QVBoxLayout()

        # Description label
        turn_description = QLabel(
            "Configure how turns are applied to different pictograph types:\n"
            "- Non-hybrid types (A, B, D, E): Turns will be applied according to your selection\n"
            "- Hybrid types (C, F): Two versions will be generated with different motion patterns"
        )
        turn_description.setWordWrap(True)
        turn_layout.addWidget(turn_description)

        # Turn selection for right hand (red)
        right_hand_layout = QHBoxLayout()
        right_hand_layout.addWidget(QLabel("Right Hand (Red) Turns:"))
        self.right_hand_combo = QComboBox()
        self.right_hand_combo.addItems(["0", "1", "2", "3"])
        self.right_hand_combo.setCurrentIndex(1)  # Default to 1 turn
        right_hand_layout.addWidget(self.right_hand_combo)
        turn_layout.addLayout(right_hand_layout)

        # Turn selection for left hand (blue)
        left_hand_layout = QHBoxLayout()
        left_hand_layout.addWidget(QLabel("Left Hand (Blue) Turns:"))
        self.left_hand_combo = QComboBox()
        self.left_hand_combo.addItems(["0", "1", "2", "3"])
        self.left_hand_combo.setCurrentIndex(0)  # Default to 0 turns
        left_hand_layout.addWidget(self.left_hand_combo)
        turn_layout.addLayout(left_hand_layout)

        # Generate all combinations checkbox
        self.generate_all_checkbox = QCheckBox(
            "Generate all turn combinations (0-3 for each hand)"
        )
        self.generate_all_checkbox.setChecked(False)
        self.generate_all_checkbox.stateChanged.connect(self._on_generate_all_changed)
        turn_layout.addWidget(self.generate_all_checkbox)

        # Turn direction selection
        turn_direction_layout = QHBoxLayout()
        turn_direction_layout.addWidget(QLabel("Turn Direction:"))
        self.turn_direction_combo = QComboBox()
        self.turn_direction_combo.addItems(["Alpha 1 to Alpha 3"])
        turn_direction_layout.addWidget(self.turn_direction_combo)
        turn_layout.addLayout(turn_direction_layout)

        turn_group.setLayout(turn_layout)
        main_layout.addWidget(turn_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Export Pictographs")
        self.export_button.clicked.connect(self._export_pictographs)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

    def _on_pictograph_checkbox_changed(self, state, letter):
        """Handle pictograph checkbox state changes."""
        self.pictograph_types_to_export[letter] = state == Qt.CheckState.Checked.value

    def _on_generate_all_changed(self, state):
        """Handle generate all combinations checkbox state changes."""
        generate_all = state == Qt.CheckState.Checked.value

        # Enable/disable the individual turn selection combos based on the checkbox
        self.right_hand_combo.setEnabled(not generate_all)
        self.left_hand_combo.setEnabled(not generate_all)

    def _export_pictographs(self):
        """Export the selected pictographs with the configured turns."""
        # Get the selected pictograph types
        selected_types = [
            letter
            for letter, selected in self.pictograph_types_to_export.items()
            if selected
        ]

        if not selected_types:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select at least one pictograph type to export.",
            )
            return

        # Ask the user for a directory to save the images
        directory = self._get_export_directory()
        if not directory:
            return  # User canceled

        # Check if we have access to the dataset
        if (
            not hasattr(self.main_widget, "pictograph_dataset")
            or not self.main_widget.pictograph_dataset
        ):
            # Fallback to codex data if dataset is not available
            codex = self.main_widget.codex
            codex_data_manager = codex.data_manager
            pictograph_data = codex_data_manager.get_pictograph_data()

            if not pictograph_data:
                QMessageBox.information(
                    self,
                    "No Pictographs",
                    "No pictographs found to export.",
                )
                return
        else:
            # Use the pictograph_dataset directly
            # Create a dictionary with letter strings as keys for compatibility
            pictograph_data = {}
            for letter_str in "ABCDEF":
                # Convert string to Letter enum
                try:
                    letter_enum = Letter(letter_str)
                    if letter_enum in self.main_widget.pictograph_dataset:
                        pictograph_data[letter_str] = letter_enum
                except ValueError:
                    # Skip if letter is not in the enum
                    continue

        # Determine if we're generating all combinations
        generate_all = self.generate_all_checkbox.isChecked()

        # Get the selected turn values
        if not generate_all:
            # Use the selected values from the combo boxes
            red_turns = int(self.right_hand_combo.currentText())
            blue_turns = int(self.left_hand_combo.currentText())
            turn_combinations = [(red_turns, blue_turns)]
        else:
            # Generate all combinations of turns (0-3 for each hand)
            turn_combinations = [(red, blue) for red in range(4) for blue in range(4)]

        # Calculate total count for progress bar
        if generate_all:
            # 16 combinations per letter (4 turns for each hand)
            total_count = len(selected_types) * 16
            # Add extra for C and F which need two versions for each combination
            if "C" in selected_types:
                total_count += 16
            if "F" in selected_types:
                total_count += 16
        else:
            # Just one combination per letter
            total_count = len(selected_types)
            # Add extra for C and F which need two versions
            if "C" in selected_types:
                total_count += 1
            if "F" in selected_types:
                total_count += 1

        # Create and configure progress dialog
        progress = QProgressDialog(
            "Exporting pictographs with turns...", "Cancel", 0, total_count, self
        )
        progress.setWindowTitle("Exporting Pictographs")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()

        try:
            exported_count = 0

            # Use diamond grid mode as default
            grid_mode = "diamond"

            # Process each selected pictograph type
            for letter in selected_types:
                if progress.wasCanceled():
                    break

                # Get the pictograph data for this letter
                data = pictograph_data.get(letter)
                if not data:
                    continue

                # Try to determine grid mode from the data
                # Check if data is a Letter enum
                if isinstance(data, Letter):
                    # For Letter enum, we'll use the default grid mode
                    current_grid_mode = grid_mode
                else:
                    # For dictionary data, try to detect the grid mode
                    detected_grid_mode = GridModeChecker.get_grid_mode(data)
                    if detected_grid_mode and detected_grid_mode != "skewed":
                        # Use the detected grid mode if available
                        current_grid_mode = detected_grid_mode
                    else:
                        # Fall back to default
                        current_grid_mode = grid_mode

                # Process each turn combination for this letter
                for red_turns, blue_turns in turn_combinations:
                    if progress.wasCanceled():
                        break

                    try:
                        # Handle different pictograph types
                        if letter in ["A", "B", "D", "E"]:
                            # Non-hybrid types: apply the specified turns
                            self._export_non_hybrid_pictograph(
                                letter,
                                data,
                                current_grid_mode,
                                directory,
                                red_turns=red_turns,
                                blue_turns=blue_turns,
                            )
                            exported_count += 1
                        elif letter in ["C", "F"]:
                            # Hybrid types: two versions with different motion patterns
                            self._export_hybrid_pictograph(
                                letter,
                                data,
                                current_grid_mode,
                                directory,
                                red_turns=red_turns,
                                blue_turns=blue_turns,
                            )
                            exported_count += 2  # Two versions

                    except Exception as e:
                        print(
                            f"Error exporting codex pictograph {letter} with turns ({red_turns}, {blue_turns}): {e}"
                        )

                    # Update progress
                    progress.setValue(exported_count)

        finally:
            progress.close()

        # Show completion message
        if exported_count > 0:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                f"Successfully exported {exported_count} codex pictographs with turns to {directory}"
            )

            # Open the directory
            os.startfile(directory)
            self.accept()
        else:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "No codex pictographs were exported."
            )

    def _export_non_hybrid_pictograph(
        self, letter, data, grid_mode, directory, red_turns=1, blue_turns=0
    ):
        """Export a non-hybrid pictograph (A, B, D, E) with specified turns."""
        # For non-hybrid pictographs, we need to find the correct one from the dataset
        # A, B should go from alpha1 to alpha3
        # D, E should go from beta1 to alpha3

        # Determine the correct start and end positions based on the letter
        if letter in ["A", "B"]:
            start_pos = "alpha1"
            end_pos = "alpha3"
        elif letter in ["D", "E"]:
            start_pos = "beta1"
            end_pos = "alpha3"
        else:
            # Default for other types
            if isinstance(data, dict):
                start_pos = data.get("start_pos")
                end_pos = data.get("end_pos")
            else:
                # If data is just the letter, use default positions
                start_pos = "alpha1"
                end_pos = "alpha3"

        # Find a matching pictograph from the dataset
        matching_pictograph = None

        # Check if data is a Letter enum (from pictograph_dataset)
        if isinstance(data, Letter) and hasattr(self.main_widget, "pictograph_dataset"):
            # Get all pictographs for this letter
            letter_pictographs = self.main_widget.pictograph_dataset.get(data, [])

            # Find one that matches the start and end positions
            for pic_data in letter_pictographs:
                if (
                    pic_data.get("start_pos") == start_pos
                    and pic_data.get("end_pos") == end_pos
                ):
                    matching_pictograph = pic_data
                    break
        # Fallback to the old method
        elif (
            hasattr(self.main_widget, "pictograph_dataset")
            and self.main_widget.pictograph_dataset
        ):
            # Try to convert string letter to enum
            try:
                letter_enum = Letter(letter)
                letter_pictographs = self.main_widget.pictograph_dataset.get(
                    letter_enum, []
                )

                for pic_data in letter_pictographs:
                    if (
                        pic_data.get("start_pos") == start_pos
                        and pic_data.get("end_pos") == end_pos
                    ):
                        matching_pictograph = pic_data
                        break
            except ValueError:
                # If letter is not in enum, try the old method
                pass

        # If we found a matching pictograph, use it
        if matching_pictograph:
            pictograph = self.codex_exporter._create_pictograph_from_data(
                matching_pictograph, grid_mode
            )
        else:
            # Fallback to the original method if we can't find a match
            print(
                f"Could not find matching pictograph for {letter} in dataset, using fallback method"
            )
            pictograph = self._create_pictograph_from_data(data, grid_mode)

        # Apply the specified turns
        self._apply_turns_to_pictograph(
            pictograph, red_turns=red_turns, blue_turns=blue_turns
        )

        # Save the pictograph with a filename that includes the turn values
        filename = f"{letter}_red{red_turns}_blue{blue_turns}.png"
        filepath = os.path.join(directory, filename)

        # Create and save image
        image = self._create_pictograph_image(pictograph)
        image.save(filepath, "PNG", 100)
        print(
            f"Saved non-hybrid pictograph {letter} with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
        )

    def _export_hybrid_pictograph(
        self, letter, data, grid_mode, directory, red_turns=1, blue_turns=0
    ):
        """Export a hybrid pictograph (C, F) with two different motion patterns."""
        # For hybrid pictographs, we need to find the two versions from the dataset
        # C should go from alpha1 to alpha3
        # F should go from beta1 to alpha3

        # Determine the correct start and end positions based on the letter
        if letter == "C":
            start_pos = "alpha1"
            end_pos = "alpha3"
        elif letter == "F":
            start_pos = "beta1"
            end_pos = "alpha3"
        else:
            # Default for other hybrid types
            if isinstance(data, dict):
                start_pos = data.get("start_pos")
                end_pos = data.get("end_pos")
            else:
                # If data is just the letter, use default positions
                start_pos = "alpha1"
                end_pos = "alpha3"

        # Find all matching pictographs from the pictograph_dataset
        matching_pictographs = []

        # Check if data is a Letter enum (from pictograph_dataset)
        if isinstance(data, Letter) and hasattr(self.main_widget, "pictograph_dataset"):
            # Get all pictographs for this letter
            letter_pictographs = self.main_widget.pictograph_dataset.get(data, [])

            # Find ones that match the start and end positions
            for pic_data in letter_pictographs:
                if (
                    pic_data.get("start_pos") == start_pos
                    and pic_data.get("end_pos") == end_pos
                ):
                    matching_pictographs.append(pic_data)
        # Fallback to the old method
        elif (
            hasattr(self.main_widget, "pictograph_dataset")
            and self.main_widget.pictograph_dataset
        ):
            # Try to convert string letter to enum
            try:
                letter_enum = Letter(letter)
                letter_pictographs = self.main_widget.pictograph_dataset.get(
                    letter_enum, []
                )

                for pic_data in letter_pictographs:
                    if (
                        pic_data.get("start_pos") == start_pos
                        and pic_data.get("end_pos") == end_pos
                    ):
                        matching_pictographs.append(pic_data)
            except ValueError:
                # If letter is not in enum, try the old method
                pass

        # If we found matching pictographs, use them
        if len(matching_pictographs) >= 2:
            # Sort by motion type to ensure we get both versions
            pro_version = None
            anti_version = None

            for pic_data in matching_pictographs:
                red_attrs = pic_data.get("red_attributes", {})
                if red_attrs.get("motion_type") == "pro":
                    pro_version = pic_data
                elif red_attrs.get("motion_type") == "anti":
                    anti_version = pic_data

            # Export the PRO version
            if pro_version:
                pictograph1 = self.codex_exporter._create_pictograph_from_data(
                    pro_version, grid_mode
                )
                self._apply_turns_to_pictograph(
                    pictograph1, red_turns=red_turns, blue_turns=blue_turns
                )

                filename1 = f"{letter}_red_pro_red{red_turns}_blue{blue_turns}.png"
                filepath1 = os.path.join(directory, filename1)

                image1 = self._create_pictograph_image(pictograph1)
                image1.save(filepath1, "PNG", 100)
                print(
                    f"Saved hybrid pictograph {letter} (Red:PRO) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath1}"
                )

            # Export the ANTI version
            if anti_version:
                pictograph2 = self.codex_exporter._create_pictograph_from_data(
                    anti_version, grid_mode
                )
                self._apply_turns_to_pictograph(
                    pictograph2, red_turns=red_turns, blue_turns=blue_turns
                )

                filename2 = f"{letter}_red_anti_red{red_turns}_blue{blue_turns}.png"
                filepath2 = os.path.join(directory, filename2)

                image2 = self._create_pictograph_image(pictograph2)
                image2.save(filepath2, "PNG", 100)
                print(
                    f"Saved hybrid pictograph {letter} (Red:ANTI) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath2}"
                )
        else:
            # Fallback to the original method if we can't find matches
            print(
                f"Could not find matching pictographs for {letter} in dataset, using fallback method"
            )

            # First version
            pictograph1 = self._create_pictograph_from_data(data, grid_mode)
            self._apply_turns_to_pictograph(
                pictograph1, red_turns=red_turns, blue_turns=blue_turns
            )

            filename1 = f"{letter}_version1_red{red_turns}_blue{blue_turns}.png"
            filepath1 = os.path.join(directory, filename1)

            image1 = self._create_pictograph_image(pictograph1)
            image1.save(filepath1, "PNG", 100)
            print(
                f"Saved hybrid pictograph {letter} (Version 1) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath1}"
            )

    def _apply_turns_to_pictograph(
        self,
        pictograph: "Pictograph",
        red_turns=0,
        blue_turns=0,
    ):
        """Apply the specified turns to a pictograph."""
        # Get the motion objects
        blue_motion = pictograph.elements.motion_set.get(BLUE)
        red_motion = pictograph.elements.motion_set.get(RED)

        # Update the pictograph data directly
        pictograph_data = pictograph.state.pictograph_data.copy()

        # Update blue motion data
        if blue_motion and BLUE + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[BLUE + "_attributes"]["turns"] = blue_turns

        # Update red motion data
        if red_motion and RED + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[RED + "_attributes"]["turns"] = red_turns

        # Apply the updated data to the pictograph
        pictograph.managers.updater.update_pictograph(pictograph_data)

        # Also set turns directly on the motion objects for good measure
        if blue_motion:
            # Only update the turns value, preserve everything else
            blue_motion.state.turns = blue_turns

        if red_motion:
            # Only update the turns value, preserve everything else
            red_motion.state.turns = red_turns

        # Update the pictograph's turns tuple
        if hasattr(pictograph.managers, "get") and hasattr(
            pictograph.managers.get, "turns_tuple"
        ):
            try:
                # This will update the turns tuple based on the new turns
                pictograph.state.turns_tuple = pictograph.managers.get.turns_tuple()
            except Exception as e:
                print(f"Error updating turns tuple: {e}")

        # Make sure the arrows are updated to reflect the turns
        if hasattr(pictograph.elements, "arrows"):
            for _, arrow in pictograph.elements.arrows.items():
                arrow.setup_components()

        # Update the pictograph
        pictograph.update()

    def _create_pictograph_from_data(self, pictograph_data, grid_mode):
        """Create a pictograph from the given data."""
        # Handle the case where pictograph_data is just a letter
        if isinstance(pictograph_data, str):
            letter = pictograph_data
            # Default positions based on letter
            if letter in ["A", "B", "C"]:
                start_pos = "alpha1"
                end_pos = "alpha3"
            elif letter in ["D", "E", "F"]:
                start_pos = "beta1"
                end_pos = "alpha3"
            else:
                start_pos = None
                end_pos = None
        else:
            # Extract data from the dictionary
            letter = pictograph_data.get("letter")
            start_pos = pictograph_data.get("start_pos")
            end_pos = pictograph_data.get("end_pos")

        # Try to find the pictograph in the main widget's pictograph_dataset
        if (
            hasattr(self.main_widget, "pictograph_dataset")
            and self.main_widget.pictograph_dataset
        ):
            # If we have a string letter, try to convert it to a Letter enum
            if isinstance(letter, str):
                try:
                    letter_enum = Letter(letter)
                    # Get all pictographs for this letter
                    letter_pictographs = self.main_widget.pictograph_dataset.get(
                        letter_enum, []
                    )

                    # Find one that matches the start and end positions
                    for pic_data in letter_pictographs:
                        if (
                            start_pos is None or pic_data.get("start_pos") == start_pos
                        ) and (end_pos is None or pic_data.get("end_pos") == end_pos):
                            # Found a matching pictograph, use it
                            return self.codex_exporter._create_pictograph_from_data(
                                pic_data, grid_mode
                            )
                except ValueError:
                    # If letter is not in enum, continue with other methods
                    pass
            # If we have a Letter enum directly
            elif isinstance(letter, Letter):
                # Get all pictographs for this letter
                letter_pictographs = self.main_widget.pictograph_dataset.get(letter, [])

                # Find one that matches the start and end positions
                for pic_data in letter_pictographs:
                    if (
                        start_pos is None or pic_data.get("start_pos") == start_pos
                    ) and (end_pos is None or pic_data.get("end_pos") == end_pos):
                        # Found a matching pictograph, use it
                        return self.codex_exporter._create_pictograph_from_data(
                            pic_data, grid_mode
                        )

        # Fallback to the original method if we can't find a match
        if isinstance(pictograph_data, str):
            # Create a minimal dictionary for the letter
            minimal_data = {"letter": pictograph_data}
            return self.codex_exporter._create_pictograph_from_data(
                minimal_data, grid_mode
            )
        else:
            return self.codex_exporter._create_pictograph_from_data(
                pictograph_data, grid_mode
            )

    def _create_pictograph_image(self, pictograph):
        """
        Create a QImage from a pictograph using a simpler approach.

        Args:
            pictograph: The pictograph to convert to an image

        Returns:
            QImage of the pictograph
        """
        # Create image with the same size as the pictograph
        size = 950  # Standard pictograph size
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        # Draw the pictograph onto the image
        painter = QPainter(image)
        pictograph.render(painter)
        painter.end()

        return image

    def _get_export_directory(self):
        """Ask the user for a directory to save the exported images."""
        return self.codex_exporter._get_export_directory()
