from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout


class PermutationDialog(QDialog):
    def __init__(self, valid_CAPs: dict):
        super().__init__()
        self.setWindowTitle("Select Permutation Type")

        self.rotation_button = QPushButton("rotated")
        self.vertical_mirror_button = QPushButton("Vertically Mirrored")
        self.horizontal_mirror_button = QPushButton("Horizontally Mirrored")
        self.color_swap_button = QPushButton("Color Swapped")

        self.rotation_button.setFixedSize(300, 50)
        self.vertical_mirror_button.setFixedSize(150, 50)
        self.horizontal_mirror_button.setFixedSize(150, 50)
        self.color_swap_button.setFixedSize(300, 50)

        self.rotation_button.clicked.connect(self.return_rotation_option)
        self.vertical_mirror_button.clicked.connect(self.return_vertical_mirror_option)
        self.horizontal_mirror_button.clicked.connect(
            self.return_horizontal_mirror_option
        )
        self.color_swap_button.clicked.connect(self.return_color_swap_option)

        mirrored_buttons_layout = QHBoxLayout()

        mirrored_buttons_layout.addWidget(self.vertical_mirror_button)
        mirrored_buttons_layout.addWidget(self.horizontal_mirror_button)

        layout = QVBoxLayout()
        layout.addWidget(self.rotation_button)
        layout.addLayout(mirrored_buttons_layout)
        layout.addWidget(self.color_swap_button)

        self.setLayout(layout)

        self.selected_option = None
        self.set_button_states(valid_CAPs)

    def set_button_states(self, valid_CAPs: dict):
        self.rotation_button.setEnabled(valid_CAPs.get("rotation", False))
        self.vertical_mirror_button.setEnabled(valid_CAPs.get("mirror", False))
        self.horizontal_mirror_button.setEnabled(valid_CAPs.get("mirror", False))
        self.color_swap_button.setEnabled(valid_CAPs.get("color_swap", False))

    def return_rotation_option(self):
        self.selected_option = "rotation"
        self.accept()

    def return_vertical_mirror_option(self):
        self.selected_option = "vertical_mirror"
        self.accept()

    def return_horizontal_mirror_option(self):
        self.selected_option = "horizontal_mirror"
        self.accept()

    def return_color_swap_option(self):
        self.selected_option = "color_swap"
        self.accept()

    def get_options(self):
        return self.selected_option
