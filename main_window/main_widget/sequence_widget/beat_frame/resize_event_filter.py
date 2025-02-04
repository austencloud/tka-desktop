from PyQt6.QtCore import QObject, QEvent


class ResizeEventFilter(QObject):
    def eventFilter(self, obj, event: "QEvent") -> bool:
        if event.type() == QEvent.Type.Resize:
            # print(f"ResizeEvent in {obj.__class__.__name__}")
            pass
        return super().eventFilter(obj, event)
