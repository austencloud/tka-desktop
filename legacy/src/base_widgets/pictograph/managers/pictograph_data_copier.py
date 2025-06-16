import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QToolTip, QApplication
from PyQt6.QtGui import QCursor, QClipboard

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class dictCopier:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

    def copy_pictograph_data(self) -> None:
        if (
            hasattr(self.pictograph.state, "pictograph_data")
            and self.pictograph.state.pictograph_data
        ):
            try:
                pictograph_json = json.dumps(
                    self.pictograph.state.pictograph_data, indent=4, ensure_ascii=False
                )

                clipboard: QClipboard = QApplication.clipboard()
                clipboard.setText(pictograph_json)

                QToolTip.showText(
                    QCursor.pos(), "Pictograph dictionary copied to clipboard.", None
                )

            except Exception as e:
                QToolTip.showText(QCursor.pos(), "Failed to copy dictionary.", None)
        else:
            QToolTip.showText(QCursor.pos(), "No dictionary to copy.", None)
