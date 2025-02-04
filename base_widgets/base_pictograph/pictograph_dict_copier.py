import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QToolTip, QApplication
from PyQt6.QtGui import QCursor, QClipboard

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographDictCopier:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

    def copy_pictograph_dict(self) -> None:
        if (
            hasattr(self.pictograph, "pictograph_dict")
            and self.pictograph.pictograph_dict
        ):
            try:
                pictograph_json = json.dumps(
                    self.pictograph.pictograph_dict, indent=4, ensure_ascii=False
                )

                clipboard: QClipboard = QApplication.clipboard()
                clipboard.setText(pictograph_json)
                indicator_label = (
                    self.pictograph.main_widget.sequence_widget.indicator_label
                )
                indicator_label.show_message("Dictionary copied to clipboard!")
                QToolTip.showText(
                    QCursor.pos(), "Pictograph dictionary copied to clipboard.", None
                )

            except Exception as e:
                print(f"Error copying pictograph_dict to clipboard: {e}")
                QToolTip.showText(QCursor.pos(), "Failed to copy dictionary.", None)
        else:
            print("No pictograph_dict available to copy.")
            QToolTip.showText(QCursor.pos(), "No dictionary to copy.", None)
