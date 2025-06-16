from typing import TYPE_CHECKING


from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )
    from legacy.src.main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.legacy_GE_pictograph_container import (
        LegacyGraphEditorPictographContainer,
    )


class GE_Pictograph(Beat):
    view: "GE_PictographView"

    def __init__(
        self, pictograph_container: "LegacyGraphEditorPictographContainer"
    ) -> None:
        super().__init__(
            pictograph_container.graph_editor.sequence_workbench.beat_frame
        )
        self.is_blank = True
        self.main_widget = pictograph_container.graph_editor.main_widget
        self.graph_editor = pictograph_container.graph_editor
