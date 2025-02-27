import json
import os
from PIL import Image, PngImagePlugin
from data.constants import *


positions_map: dict[tuple[str], str] = {
    (SOUTH, NORTH): ALPHA1,
    (SOUTHWEST, NORTHEAST): ALPHA2,
    (WEST, EAST): ALPHA3,
    (NORTHWEST, SOUTHEAST): ALPHA4,
    (NORTH, SOUTH): ALPHA5,
    (NORTHEAST, SOUTHWEST): ALPHA6,
    (EAST, WEST): ALPHA7,
    (SOUTHEAST, NORTHWEST): ALPHA8,
    (NORTH, NORTH): BETA1,
    (NORTHEAST, NORTHEAST): BETA2,
    (EAST, EAST): BETA3,
    (SOUTHEAST, SOUTHEAST): BETA4,
    (SOUTH, SOUTH): BETA5,
    (SOUTHWEST, SOUTHWEST): BETA6,
    (WEST, WEST): BETA7,
    (NORTHWEST, NORTHWEST): BETA8,
    (WEST, NORTH): GAMMA1,
    (NORTHWEST, NORTHEAST): GAMMA2,
    (NORTH, EAST): GAMMA3,
    (NORTHEAST, SOUTHEAST): GAMMA4,
    (EAST, SOUTH): GAMMA5,
    (SOUTHEAST, SOUTHWEST): GAMMA6,
    (SOUTH, WEST): GAMMA7,
    (SOUTHWEST, NORTHWEST): GAMMA8,
    (EAST, NORTH): GAMMA9,
    (SOUTHEAST, NORTHEAST): GAMMA10,
    (SOUTH, EAST): GAMMA11,
    (SOUTHWEST, SOUTHEAST): GAMMA12,
    (WEST, SOUTH): GAMMA13,
    (NORTHWEST, SOUTHWEST): GAMMA14,
    (NORTH, WEST): GAMMA15,
    (NORTHEAST, NORTHWEST): GAMMA16,
}


def verify_and_correct_positions(metadata: dict) -> dict:
    """Verifies and corrects numbered positions based on blue and red attributes' start and end locations."""
    if "sequence" in metadata:
        for beat in metadata["sequence"]:
            if isinstance(beat, dict) and "start_pos" in beat and "end_pos" in beat:
                # Extract blue and red start and end locations
                start_tuple = (
                    beat[BLUE_ATTRIBUTES]["start_loc"],
                    beat[RED_ATTRIBUTES]["start_loc"],
                )
                end_tuple = (
                    beat[BLUE_ATTRIBUTES]["end_loc"],
                    beat[RED_ATTRIBUTES]["end_loc"],
                )

                # Determine correct positions based on the attributes
                correct_start_pos = positions_map.get(start_tuple)
                correct_end_pos = positions_map.get(end_tuple)

                # Update start_pos and end_pos only if they are incorrect
                if correct_start_pos and beat["start_pos"] != correct_start_pos:
                    beat["start_pos"] = correct_start_pos
                if correct_end_pos and beat["end_pos"] != correct_end_pos:
                    beat["end_pos"] = correct_end_pos

    return metadata


def update_file(file_path: str):
    """Updates metadata within a given image file."""
    with Image.open(file_path) as img:
        metadata = json.loads(img.info.get("metadata", "{}"))
        updated_metadata = verify_and_correct_positions(metadata)

        # Save updated metadata
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("metadata", json.dumps(updated_metadata))
        img.save(file_path, pnginfo=pnginfo)


def update_all_files_in_directory(directory: str):
    """Iterates through a directory to update all dictionary files with corrected positions."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):  # Assuming metadata is stored in PNG files
                update_file(os.path.join(root, file))
                print(f"Updated metadata in {file}")
        print(f"Updated metadata in all files in {root}")


# Example usage
dictionary_path = r"C:\Users\Austen\Desktop\the-kinetic-constructor\dictionary"
update_all_files_in_directory(dictionary_path)
