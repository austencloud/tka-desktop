import os
import stat


def remove_readonly_and_hidden(directory):
    """Recursively remove read-only or hidden attributes from files and directories."""
    for dirpath, dirnames, filenames in os.walk(directory):
        for name in dirnames + filenames:
            full_path = os.path.join(dirpath, name)
            # Get the file or directory attributes
            attrs = os.stat(full_path).st_file_attributes
            # If it's read-only or hidden, remove those attributes
            if attrs & (stat.FILE_ATTRIBUTE_READONLY | stat.FILE_ATTRIBUTE_HIDDEN):
                print(f"Removing read-only or hidden attributes from: {full_path}")
                os.chmod(full_path, stat.S_IWRITE)  # Remove read-only
                os.system(f'attrib -H "{full_path}"')  # Remove hidden attribute


root_dir = r"F:\CODE\tka-sequence-constructor\dictionary"
remove_readonly_and_hidden(root_dir)
