import os
import sys


def print_directory_tree(path, indent="", output_file=None):
    """Prints the directory tree starting from the given path to a file."""
    try:
        items = os.listdir(path)
    except OSError as e:
        print(f"{indent} [error opening dir]", file=output_file)
        return

    # Filter out .git directory and other unnecessary files/directories
    items = [
        item
        for item in items
        if item != ".git" and item != ".DS_Store" and item != "node_modules"
    ]

    # If more than 20 items, show only the first 20 and then "..."
    if len(items) > 20:
        items_to_show = items[:20]
        remaining_count = len(items) - 20
    else:
        items_to_show = items
        remaining_count = 0

    for i, item in enumerate(items_to_show):
        item_path = os.path.join(path, item)
        is_last = i == len(items_to_show) - 1
        if os.path.isdir(item_path):
            print(
                indent + ("└── " if is_last else "├── ") + item + "/", file=output_file
            )
            print_directory_tree(
                item_path, indent + ("    " if is_last else "│   "), output_file
            )
        else:
            print(indent + ("└── " if is_last else "├── ") + item, file=output_file)

    if remaining_count > 0:
        print(
            indent + "└── ... (" + str(remaining_count) + " more items)",
            file=output_file,
        )  # Indicate remaining files


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = "."  # Current directory if no argument is provided

    with open("tree.txt", "w", encoding="utf-8") as f:
        print_directory_tree(start_path, output_file=f)
