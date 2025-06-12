class StyleManager:
    @staticmethod
    def get_gradient_background(theme="dark"):
        if theme == "dark":
            return """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:0.3 #1a1a1e, stop:0.7 #16213e, stop:1 #0f0f23);
            """
        else:
            return """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:0.3 #e9ecef, stop:0.7 #dee2e6, stop:1 #f8f9fa);
            """

    @staticmethod
    def get_button_style(variant="default", compact=False, state="default"):
        base_radius = "15px" if compact else "18px"
        base_padding = "8px" if compact else "12px"
        base_font_size = "12px" if compact else "14px"

        styles = {
            "default": f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.12), 
                        stop:0.5 rgba(102, 126, 234, 0.1), 
                        stop:1 rgba(118, 75, 162, 0.1));
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: {base_radius};
                    color: white;
                    font-size: {base_font_size};
                    font-weight: 700;
                    text-align: center;
                    padding: {base_padding};
                    font-family: 'Segoe UI';
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.18), 
                        stop:0.5 rgba(102, 126, 234, 0.15), 
                        stop:1 rgba(118, 75, 162, 0.15));
                    border: 2px solid rgba(255, 255, 255, 0.3);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.08), 
                        stop:0.5 rgba(102, 126, 234, 0.08), 
                        stop:1 rgba(118, 75, 162, 0.08));
                    border: 2px solid rgba(255, 255, 255, 0.15);
                }}
            """,
            "running": f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(46, 204, 113, 0.2), 
                        stop:0.5 rgba(39, 174, 96, 0.15), 
                        stop:1 rgba(46, 204, 113, 0.1));
                    border: 2px solid rgba(46, 204, 113, 0.4);
                    border-radius: {base_radius};
                    color: #2ecc71;
                    font-size: {base_font_size};
                    font-weight: 700;
                    text-align: center;
                    padding: {base_padding};
                    font-family: 'Segoe UI';
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(46, 204, 113, 0.3), 
                        stop:0.5 rgba(39, 174, 96, 0.25), 
                        stop:1 rgba(46, 204, 113, 0.2));
                    border: 2px solid rgba(46, 204, 113, 0.6);
                }}
            """,
            "compact": f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: {base_radius};
                    color: white;
                    font-size: {base_font_size};
                    font-weight: 600;
                    padding: {base_padding};
                    font-family: 'Segoe UI';
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }}
            """,
        }
        return styles.get(variant, styles["default"])

    @staticmethod
    def get_group_style(compact=False):
        padding = "8px" if compact else "12px"
        margin = "4px" if compact else "8px"
        return f"""
            QGroupBox {{
                font-weight: 700;
                font-size: 14px;
                color: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin-top: 1ex;
                padding: {padding};
                margin: {margin};
                background: rgba(255, 255, 255, 0.05);
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }}
        """

    @staticmethod
    def get_tab_style():
        return """
            QTabWidget::pane {
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.02);
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: rgba(255, 255, 255, 0.7);
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: rgba(102, 126, 234, 0.2);
                color: white;
                border-bottom: 2px solid #667eea;
            }
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.15);
                color: rgba(255, 255, 255, 0.9);
            }
        """
