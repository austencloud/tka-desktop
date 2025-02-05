import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QToolTip, QApplication
from PyQt6.QtGui import QCursor, QClipboard

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph


class PictographDictCopier:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def copy_pictograph_data(self) -> None:
        if (
            hasattr(self.pictograph, "pictograph_data")
            and self.pictograph.pictograph_data
        ):
            try:
                pictograph_json = json.dumps(
                    self.pictograph.pictograph_data, indent=4, ensure_ascii=False
                )

                clipboard: QClipboard = QApplication.clipboard()
                clipboard.setText(pictograph_json)
                indicator_label = (
                    self.pictograph.main_widget.sequence_workbench.indicator_label
                )
                indicator_label.show_message("Dictionary copied to clipboard!")
                QToolTip.showText(
                    QCursor.pos(),
                    "BasePictograph dictionary copied to clipboard.",
                    None,
                )

            except Exception as e:
                print(f"Error copying pictograph_data to clipboard: {e}")
                QToolTip.showText(QCursor.pos(), "Failed to copy dictionary.", None)
        else:
            print("No pictograph_data available to copy.")
            QToolTip.showText(QCursor.pos(), "No dictionary to copy.", None)
