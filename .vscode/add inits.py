import os


def add_init_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        init_path = os.path.join(dirpath, "__init__.py")
        if not os.path.exists(init_path):
            open(init_path, "w").close()  # Create an empty __init__.py file


# Change 'src' to your actual source directory
project_root = os.path.join(os.getcwd(), "src")
add_init_files(project_root)

print("✅ All necessary __init__.py files have been created!")
