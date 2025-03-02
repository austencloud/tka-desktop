from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


from .base_sidebar_section import BaseSidebarSection


class SidebarLevelSection(BaseSidebarSection):
    def create_widgets(self, sections_data):
        """
        Example: We show "Level" header + a line, then buttons for "1", "2", "3".
        """
        level_label = QLabel("Level")
        self.style_header_label(level_label)
        self.manager.layout.addWidget(level_label)
        self._widgets_created.append(level_label)

        line_label = QLabel()
        line_label.setStyleSheet("border: 1px solid black;")
        self.manager.layout.addWidget(line_label)
        self._widgets_created.append(line_label)

        for lvl in ["1", "2", "3"]:
            btn = QPushButton(lvl)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(
                lambda _, lv=lvl, b=btn: self.manager.scroll_to_section(lv, b)
            )
            self.manager.layout.addWidget(btn)
            self._widgets_created.append(btn)
            self.manager.buttons.append(btn)
