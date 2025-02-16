from typing import TYPE_CHECKING
from data.constants import BLUE, RED
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from ..settings_manager import SettingsManager


class PropTypeChanger:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.main_window = settings_manager.main_window

    def replace_props(self, new_prop_type, pictograph: "Pictograph"):
        for color, prop in pictograph.props.items():
            new_prop = pictograph.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type
            )
            self._update_pictograph_prop(pictograph, color, new_prop)
        self._finalize_pictograph_update(pictograph)

    def _update_pictograph_prop(
        self, pictograph: "Pictograph", color, new_prop: "Prop"
    ):
        old_prop = pictograph.props[color]
        if hasattr(old_prop, "loc"):
            old_prop.deleteLater()
            old_prop.hide()
            old_prop_data = old_prop.prop_data
            pictograph.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.motions[color].prop = new_prop
            new_prop.motion.attr_manager.update_prop_ori()
            new_prop.updater.update_prop(old_prop_data)

    def _finalize_pictograph_update(self, pictograph: "Pictograph"):
        pictograph.red_prop = pictograph.props[RED]
        pictograph.blue_prop = pictograph.props[BLUE]
        pictograph.updater.update_pictograph()

    def apply_prop_type(self) -> None:
        prop_type = self.settings_manager.global_settings.get_prop_type()
        self.update_props_to_type(prop_type)

    def update_props_to_type(self, new_prop_type) -> None:
        pictographs = self._collect_all_pictographs()
        for pictograph in pictographs:
            if pictograph:
                self.replace_props(new_prop_type, pictograph)
                pictograph.prop_type = new_prop_type
                pictograph.updater.update_pictograph()

        self._update_start_pos_view(new_prop_type)
        self._update_json_manager(new_prop_type)

    def _collect_all_pictographs(self) -> list["Pictograph"]:
        main_widget = self.main_window.main_widget
        pictographs = set()

        # Collect pictographs from the pictograph cache
        for pictograph_list in main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if pictograph.view:
                    pictographs.add(pictograph)

        # Collect pictographs from the sequence widget's beat frame
        for beat_view in main_widget.sequence_workbench.beat_frame.beat_views:
            if beat_view.is_filled:
                pictographs.add(beat_view.beat)

        # Collect pictographs from the construct tab's option picker
        pictographs.update(main_widget.construct_tab.option_picker.option_pool)

        # Collect pictographs from the learn tab's codex section manager
        for (
            codex_view
        ) in main_widget.learn_tab.codex.section_manager.codex_views.values():
            pictographs.add(codex_view.pictograph)

        # Collect the graph editor's pictograph
        graph_editor_pictograph = (
            main_widget.sequence_workbench.graph_editor.pictograph_container.GE_view.pictograph
        )
        if graph_editor_pictograph.red_arrow.loc:
            pictographs.add(graph_editor_pictograph)

        lesson_1_pictograph = (
            main_widget.learn_tab.lesson_1_widget.question_widget.pictograph
        )
        pictographs.add(lesson_1_pictograph)

        lesson_2_question_pictograph = (
            main_widget.learn_tab.lesson_2_widget.question_widget.pictograph
        )
        lesson_2_answer_pictographs = (
            main_widget.learn_tab.lesson_2_widget.answers_widget.pictographs
        )
        pictographs.add(lesson_2_question_pictograph)
        pictographs.update(lesson_2_answer_pictographs.values())

        lesson_3_question_pictograph = (
            main_widget.learn_tab.lesson_3_widget.question_widget.pictograph
        )
        lesson_3_answer_pictographs = (
            main_widget.learn_tab.lesson_3_widget.answers_widget.pictographs
        )
        pictographs.add(lesson_3_question_pictograph)
        pictographs.update(lesson_3_answer_pictographs.values())
        pictograph_list: list["Pictograph"] = list(pictographs)

        pictograph_list = [pictograph for pictograph in pictograph_list if pictograph]

        pictograph_list = [
            pictograph
            for pictograph in pictograph_list
            if hasattr(pictograph.red_prop, "loc")
            and hasattr(pictograph.blue_prop, "loc")
        ]

        return pictograph_list

    def _update_start_pos_view(self, new_prop_type):
        start_pos_view = (
            self.main_window.main_widget.sequence_workbench.beat_frame.start_pos_view
        )
        if hasattr(start_pos_view, "start_pos"):
            start_pos = start_pos_view.start_pos
            if start_pos.view.is_filled:
                self.replace_props(new_prop_type, start_pos)

    def _update_json_manager(self, new_prop_type):
        json_manager = self.main_window.main_widget.json_manager
        json_manager.updater.prop_type_updater.update_prop_type_in_json(new_prop_type)
