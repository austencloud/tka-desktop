from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_pictograph_container import (
        GraphEditorPictographContainer,
    )


class GE_Pictograph(Beat):
    def __init__(self, pictograph_container: "GraphEditorPictographContainer") -> None:
        super().__init__(
            pictograph_container.graph_editor.sequence_workbench.sequence_beat_frame
        )
        self.is_blank = True
