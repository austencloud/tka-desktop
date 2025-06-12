class StyleManager:
    @staticmethod
    def get_gradient_background():
        return """
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2c3e50, stop:0.3 #34495e, stop:0.7 #2c3e50, stop:1 #1a252f);
        """

    @staticmethod
    def get_card_style():
        return """
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                padding: 12px;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.12);
                border-color: rgba(74, 144, 226, 0.6);
            }
        """

    @staticmethod
    def get_button_style(variant="default", compact=False):
        size = "32px" if compact else "40px"
        padding = "6px 12px" if compact else "8px 16px"
        font_size = "11px" if compact else "12px"

        if variant == "primary":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a90e2, stop:1 #357abd);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: {padding};
                    min-height: {size};
                    font-size: {font_size};
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5ba0f2, stop:1 #458acd);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a80d2, stop:1 #2570ad);
                }}
            """
        elif variant == "running":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #27ae60, stop:1 #1e8449);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: {padding};
                    min-height: {size};
                    font-size: {font_size};
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2ecc71, stop:1 #239b56);
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                    padding: {padding};
                    min-height: {size};
                    font-size: {font_size};
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.15);
                    border-color: rgba(255, 255, 255, 0.3);
                }}
                QPushButton:pressed {{
                    background: rgba(255, 255, 255, 0.05);
                }}
            """

    @staticmethod
    def get_tab_style():
        return """
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.8);
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: rgba(74, 144, 226, 0.3);
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.1);
            }
        """

    @staticmethod
    def get_search_style():
        return """
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 8px 16px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: rgba(74, 144, 226, 0.6);
                background: rgba(255, 255, 255, 0.15);
            }
        """

    @staticmethod
    def get_group_style(compact=False):
        padding = "10px 15px 15px 15px" if compact else "15px 20px 20px 20px"
        font_size = "12px" if compact else "14px"

        return f"""
            QGroupBox {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                font-weight: bold;
                font-size: {font_size};
                color: white;
                padding-top: 18px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background: transparent;
                color: rgba(255, 255, 255, 0.9);
            }}
        """

    @staticmethod
    def get_main_style():
        return (
            """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:0.3 #34495e, stop:0.7 #2c3e50, stop:1 #1a252f);
                color: white;
            }
        """
            + StyleManager.get_button_style()
            + StyleManager.get_tab_style()
            + StyleManager.get_search_style()
        )
