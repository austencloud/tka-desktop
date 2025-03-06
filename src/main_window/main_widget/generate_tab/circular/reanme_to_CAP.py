import os

def rename_files_and_directories(directory):
    for root, directories, files in os.walk(directory):
        # Rename files
        for filename in files:
            if "permutation" in filename:
                old_file_path = os.path.join(root, filename)
                new_filename = filename.replace("permutation", "CAP")
                new_file_path = os.path.join(root, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f'Renamed file: "{filename}" -> "{new_filename}"')

        # Rename directories
        for dirname in directories:
            if "permutation" in dirname:
                old_dir_path = os.path.join(root, dirname)
                new_dirname = dirname.replace("permutation", "CAP")
                new_dir_path = os.path.join(root, new_dirname)
                os.rename(old_dir_path, new_dir_path)
                print(f'Renamed directory: "{dirname}" -> "{new_dirname}"')

if __name__ == "__main__":
    directory = "F:\\CODE\\the-kinetic-constructor-desktop\\src"
    rename_files_and_directories(directory)
    print("Renaming completed.")
