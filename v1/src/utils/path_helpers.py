import sys
import os
import winreg


def get_data_path(filename) -> str:
    """
    Dynamically resolve the correct data path.

    This function tries to find the specified file in multiple possible locations.
    It first checks if the file exists in each location before returning the path.
    """
    if hasattr(sys, "_MEIPASS"):  # PyInstaller uses _MEIPASS for the temp folder
        base_dir = os.path.join(sys._MEIPASS, "src", "data")
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # Try V1-specific paths first, then legacy paths
    possible_paths = [
        # V1-specific paths (prioritized)
        os.path.abspath(os.path.join(os.getcwd(), "v1", "data")),  # From project root
        os.path.abspath(os.path.join(os.getcwd(), "data")),  # From v1/ directory
        os.path.abspath(
            os.path.join(os.path.dirname(os.getcwd()), "v1", "data")
        ),  # From subdirectory
        # Legacy paths for compatibility
        os.path.abspath(os.path.join(os.getcwd(), "src", "data")),
        os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "data")),
        os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "src", "data")),
        os.path.abspath(os.path.join(os.getcwd(), "..", "data")),
        os.path.abspath(os.path.join(os.getcwd(), "..", "src", "data")),
    ]

    # Check each possible path for the specific file
    for base_dir in possible_paths:
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # If the file is not found in any of the possible locations,
    # return the default path (even if the file doesn't exist there)
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "data"))
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)


def get_image_path(filename) -> str:
    """
    Dynamically resolve the correct images path.

    This function tries to find the specified file in multiple possible locations.
    It first checks if the file exists in each location before returning the path.
    If the file is not found, it returns a path where the file should be.
    """
    # Normalize the filename to use forward slashes
    filename = filename.replace("\\", "/")

    if hasattr(sys, "_MEIPASS"):  # PyInstaller uses _MEIPASS for the temp folder
        base_dir = os.path.join(sys._MEIPASS, "src", "images")
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # Try V1-specific image paths first, then legacy paths
    possible_paths = [
        # V1-specific paths (prioritized)
        os.path.abspath(os.path.join(os.getcwd(), "v1", "images")),  # From project root
        os.path.abspath(os.path.join(os.getcwd(), "images")),  # From v1/ directory
        os.path.abspath(
            os.path.join(os.path.dirname(os.getcwd()), "v1", "images")
        ),  # From subdirectory
        # Legacy paths for compatibility
        os.path.abspath(os.path.join(os.getcwd(), "src", "images")),
        os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "images")),
        os.path.abspath(os.path.join(os.getcwd(), "..", "images")),
        os.path.abspath(os.path.join(os.getcwd(), "data", "images")),
        os.path.abspath(os.path.join(os.getcwd(), "src", "data", "images")),
    ]

    # Check each possible path for the specific file
    for base_dir in possible_paths:
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # If the file is not found in any of the possible locations,
    # create the default directory and return the path (even if the file doesn't exist)
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "images"))

    # Create the directory structure for the file
    dir_path = os.path.dirname(os.path.join(base_dir, filename))
    os.makedirs(dir_path, exist_ok=True)

    return os.path.join(base_dir, filename)


def get_settings_path():
    """
    Returns the correct settings.ini path.

    - In development mode, it reads from the root directory.
    - In a packaged PyInstaller executable, it reads from AppData.
    """
    if getattr(sys, "frozen", False):  # Running as a packaged EXE
        return get_app_data_path("settings.ini")
    else:  # Development mode
        return os.path.join(os.getcwd(), "settings.ini")


def get_app_data_path(filename) -> str:
    """
    For use in a Windows environment, this will return the path to the appdata directory.

    This is used for files that the user will modify, such as:
    - current_sequence json
    - settings json
    - saved words
    """
    appdata_dir = os.path.join(os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet")
    os.makedirs(appdata_dir, exist_ok=True)  # Make sure the directory exists
    return os.path.join(appdata_dir, filename)


def get_dev_path(filename) -> str:
    """
    For use in a development environment, this will return the path to the current working directory.

    This is used for files that the user will modify, such as:
    - current_sequence json
    - settings json
    - saved words
    """

    base_path = os.path.abspath(".")
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, filename)


def get_user_editable_resource_path(filename) -> str:
    if getattr(sys, "frozen", False):
        path = get_app_data_path(filename)
    else:
        path = get_dev_path(filename)
    return path


def get_dictionary_path() -> str:
    """
    Returns the path to the dictionary directory.

    In development mode, it tries multiple possible locations.
    In a packaged PyInstaller executable, it uses the AppData directory.
    """
    if getattr(sys, "frozen", False):
        # For packaged executable
        dictionary_path = os.path.join(
            os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "dictionary"
        )
    else:
        # For development mode, try multiple possible locations
        possible_paths = [
            os.path.abspath(os.path.join(os.getcwd(), "data", "dictionary")),
            os.path.abspath(os.path.join(os.getcwd(), "src", "data", "dictionary")),
            os.path.abspath(
                os.path.join(os.path.dirname(os.getcwd()), "data", "dictionary")
            ),
            os.path.abspath(os.path.join(os.getcwd(), "..", "data", "dictionary")),
            os.path.abspath(os.path.join(os.getcwd(), "dictionary")),
            os.path.abspath(os.path.join(os.getcwd(), "browse")),  # Legacy path
        ]

        # Use the first path that exists
        dictionary_path = None
        for path in possible_paths:
            if os.path.exists(path):
                dictionary_path = path
                break

        # If no existing path is found, use the default
        if dictionary_path is None:
            dictionary_path = os.path.abspath(
                os.path.join(os.getcwd(), "data", "dictionary")
            )

    # Make sure the directory exists
    os.makedirs(dictionary_path, exist_ok=True)
    return dictionary_path


def get_win32_special_folder_path(folder_name) -> str:
    """
    Returns the path to the user's custom folder on Windows.
    This folder is set by the user via the Explorer.
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        ) as key:
            folder_dir, _ = winreg.QueryValueEx(key, folder_name)
            folder_dir = os.path.expandvars(folder_dir)
    except FileNotFoundError:
        # Fallback to default locations if registry key not found
        if folder_name == "My Video":
            folder_dir = os.path.join(os.path.expanduser("~"), "Videos")
        elif folder_name == "My Pictures":
            folder_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        else:
            folder_dir = os.path.expanduser("~")

    os.makedirs(folder_dir, exist_ok=True)
    return folder_dir


def get_my_special_folder_path(folder_name, filename) -> str:
    """
    Returns the full path to a file in the user's custom folder.
    """
    folder_dir = get_win32_special_folder_path(folder_name)
    return os.path.join(folder_dir, filename)


def get_win32_videos_path() -> str:
    """
    Returns the path to the user's custom videos directory on Windows.
    This directory is set by the user via the Explorer.I. I.
    """
    videos_dir = get_win32_special_folder_path("My Video")
    tka_dir = os.path.join(videos_dir, "The Kinetic Alphabet")
    os.makedirs(tka_dir, exist_ok=True)
    return tka_dir


def get_win32_photos_path() -> str:
    """
    Returns the path to the user's custom photos directory on Windows.
    This directory is set by the user via the Explorer.
    """
    photos_dir = get_win32_special_folder_path("My Pictures")
    tka_dir = os.path.join(photos_dir, "The Kinetic Alphabet")
    os.makedirs(tka_dir, exist_ok=True)
    return tka_dir


def get_my_videos_path(filename) -> str:
    """
    Returns the full path to a file in the user's videos directory.
    """
    videos_dir = get_win32_videos_path()
    full_vid_dir = os.path.join(videos_dir, filename).replace("\\", "/")
    return full_vid_dir


def get_my_photos_path(filename) -> str:
    """
    Returns the full path to a file in the user's photos directory.
    """
    photos_dir = get_win32_photos_path()
    full_photos_dir = os.path.join(photos_dir, filename).replace("\\", "/")
    return full_photos_dir


def get_sequence_card_image_exporter_path() -> str:
    """
    Returns the path to the directory where all images with headers and footers are exported.
    """
    if getattr(sys, "frozen", False):
        export_path = get_my_photos_path("images\\sequence_card_images")
    else:
        export_path = get_dev_path("images\\sequence_card_images")
    os.makedirs(export_path, exist_ok=True)
    return export_path


def get_sequence_card_cache_path() -> str:
    """
    Returns the path to the directory where sequence card cache data is stored.

    This is always in the AppData directory to ensure persistence between sessions.
    """
    cache_dir = os.path.join(
        os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "cache", "sequence_cards"
    )
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir
