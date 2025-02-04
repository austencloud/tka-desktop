import os
import re

# Directory containing all the images
root_dir = r"F:\CODE\the_kinetic_constructor\images\sequence_card_images"

# Regular expression to match the trailing numbers in parentheses and the underscore
pattern = re.compile(r'_\(\d.*\)\.png$')

def rename_images_in_directory(directory):
    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            # Check if the file matches the pattern (underscore followed by numbers in parentheses)
            if pattern.search(filename):
                # Create the new filename by removing the parentheses and its content, along with the underscore
                new_filename = re.sub(r'_\(.+\)', '', filename).strip()

                # Ensure no double '.png' issue
                if not new_filename.endswith('.png'):
                    new_filename += ".png"
                
                # Create full paths for the old and new filenames
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

if __name__ == "__main__":
    rename_images_in_directory(root_dir)
