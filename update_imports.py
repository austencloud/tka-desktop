#!/usr/bin/env python3
import os
import re

def update_file(file_path):
    """Update the AppContext import in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the import statement
        updated_content = re.sub(
            r'from settings_manager\.global_settings\.app_context import AppContext',
            r'from src.settings_manager.global_settings.app_context import AppContext',
            content
        )
        
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes needed: {file_path}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

def main():
    """Find and update all files with the old import pattern."""
    # List of files to update (from grep output)
    files_to_update = [
        "src/base_widgets/pictograph/managers/updater/pictograph_updater.py",
        "src/main_window/main_widget/browse_tab/browse_tab_filter_controller.py",
        "src/main_window/main_widget/browse_tab/browse_tab_persistence_manager.py",
        "src/main_window/main_widget/browse_tab/browse_tab_ui_updater.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/control_panel/sort_widget/sequence_picker_sort_controller.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/control_panel/sort_widget/sequence_picker_sort_widget.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/control_panel/sort_widget/sort_buttons_bar.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/filter_stack/author_section.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/filter_stack/contains_letter_section.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/nav_sidebar/nav_sidebar_manager.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/nav_sidebar/sequence_picker_nav_sidebar.py",
        "src/main_window/main_widget/browse_tab/sequence_picker/nav_sidebar/sidebar_button_ui_updater.py",
        "src/main_window/main_widget/browse_tab/temp_beat_frame/temp_beat_frame.py",
        "src/main_window/main_widget/browse_tab/temp_beat_frame/temp_beat_frame_layout_manager.py",
        "src/main_window/main_widget/browse_tab/thumbnail_box/favorite_button.py",
        "src/main_window/main_widget/browse_tab/thumbnail_box/thumbnail_box_header.py",
        "src/main_window/main_widget/browse_tab/thumbnail_box/variation_number_label.py",
        "src/main_window/main_widget/fade_manager/fade_manager.py",
        "src/main_window/main_widget/generate_tab/freeform/letter_type_picker_widget/letter_type_picker_widget.py",
        "src/main_window/main_widget/json_manager/json_sequence_updater/json_turns_updater.py",
        "src/main_window/main_widget/json_manager/sequence_data_loader_saver.py",
        "src/main_window/main_widget/main_widget_tab_switcher.py",
        "src/main_window/main_widget/main_widget_ui.py",
        "src/main_window/main_widget/sequence_properties_manager/sequence_properties_manager.py",
        "src/main_window/main_widget/sequence_workbench/add_to_dictionary_manager/dictionary_service.py",
        "src/main_window/main_widget/sequence_workbench/base_sequence_modifier.py",
        "src/main_window/main_widget/sequence_workbench/beat_deleter/beat_deleter.py",
        "src/main_window/main_widget/sequence_workbench/full_screen_viewer.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/ori_picker_box/ori_picker_widget/ori_picker_widget.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/turns_adjustment_manager/json_turns_repository.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/turns_adjustment_manager/turns_adjustment_manager.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/turns_box/turns_widget/turns_widget.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/arrow_selection_manager.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/graph_editor_view_key_event_handler.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_adapter.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_creator.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_data_prep.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_factory.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_rot_angle_manager.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_service.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/mirrored_entry_utils.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/mirrored_entry_manager/special_placement_repository.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/special_placement_data_updater.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/data_updater/special_placement_entry_remover.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/prop_placement_override_manager.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/rot_angle_override_data_handler.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/rot_angle_override_mirror_handler.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/rot_angle_override_validator.py",
        "src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/rot_angle_override_view_updater.py",
        "src/main_window/main_widget/sequence_workbench/labels/circular_sequence_indicator.py",
        "src/main_window/main_widget/sequence_workbench/labels/workbench_difficulty_label.py",
        "src/main_window/main_widget/sequence_workbench/sequence_beat_frame/beat_adder.py",
        "src/main_window/main_widget/sequence_workbench/sequence_beat_frame/beat_frame_layout_manager.py",
        "src/main_window/main_widget/sequence_workbench/sequence_beat_frame/beat_frame_populator.py",
        "src/main_window/main_widget/sequence_workbench/sequence_color_swapper.py",
        "src/main_window/main_widget/sequence_workbench/sequence_reflector.py",
        "src/main_window/main_widget/sequence_workbench/sequence_rotater.py",
        "src/main_window/main_widget/settings_dialog/settings_dialog.py",
        "src/main_window/main_widget/settings_dialog/ui/beat_layout/layout_controls/layout_selector/layout_selector.py",
        "src/main_window/main_widget/settings_dialog/ui/beat_layout/length_selector/length_selector.py",
        "src/main_window/main_widget/settings_dialog/ui/codex_exporter/turn_applier.py",
        "src/main_window/main_widget/settings_dialog/ui/settings_dialog_tab_manager.py",
        "src/main_window/main_widget/write_tab/act_sheet/act_header/act_header.py",
        "src/main_window/main_widget/write_tab/act_sheet/act_sheet.py",
        "src/main_window/main_widget/write_tab/act_sheet/act_splitter/act_beat_scroll/act_beat_frame/act_beat_frame_layout_manager.py",
        "src/main_window/main_widget/write_tab/act_sheet/act_splitter/act_beat_scroll/act_beat_frame/act_populator.py",
        "src/objects/arrow/managers/rot_angle_manager/calculators/base_rot_angle_calculator.py",
        "src/objects/glyphs/elemental_glyph/elemental_glyph.py",
        "src/objects/glyphs/reversal_glyph.py",
        "src/objects/glyphs/start_to_end_pos_glyph/start_to_end_pos_glyph.py",
        "src/objects/glyphs/tka_glyph/tka_glyph.py",
        "src/objects/glyphs/vtg_glyph/vtg_glyph.py",
        "src/placement_managers/prop_placement_manager/handlers/beta_offset_calculator.py",
        "src/placement_managers/prop_placement_manager/handlers/swap_beta_handler.py",
    ]
    
    # Special case for prop_placement_manager.py which has the import inside a function
    prop_placement_manager_path = "src/placement_managers/prop_placement_manager/prop_placement_manager.py"
    try:
        with open(prop_placement_manager_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the import statement inside the function
        updated_content = re.sub(
            r'from settings_manager\.global_settings\.app_context import AppContext',
            r'from src.settings_manager.global_settings.app_context import AppContext',
            content
        )
        
        if content != updated_content:
            with open(prop_placement_manager_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {prop_placement_manager_path}")
        else:
            print(f"No changes needed: {prop_placement_manager_path}")
    except Exception as e:
        print(f"Error updating {prop_placement_manager_path}: {e}")
    
    # Update all the files
    for file_path in files_to_update:
        update_file(file_path)
    
    print("Import update completed!")

if __name__ == "__main__":
    main()
