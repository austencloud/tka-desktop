import os


# Function to print the directory structure in a tree-like format
def print_directory_tree(startpath, indent_level=0):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")


# Path to the root directory you want to inspect
directory_path = r"F:\CODE\tka-sequence-constructor\dictionary"

# Printing the directory tree
print_directory_tree(directory_path)
