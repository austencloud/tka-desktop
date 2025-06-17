import sys
import os
import winreg


def get_data_path(filename) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_dir = os.path.join(sys._MEIPASS, "src", "data")
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # Always use root data directory as single source of truth
    root_data_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
    )

    full_path = os.path.join(root_data_dir, filename)
    if os.path.exists(full_path):
        return full_path

    os.makedirs(root_data_dir, exist_ok=True)
    return full_path


def get_image_path(filename) -> str:
    filename = filename.replace("\\", "/")

    if hasattr(sys, "_MEIPASS"):
        base_dir = os.path.join(sys._MEIPASS, "src", "images")
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path

    # Always use root images directory as single source of truth
    root_images_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "images")
    )

    full_path = os.path.join(root_images_dir, filename)
    if os.path.exists(full_path):
        return full_path

    dir_path = os.path.dirname(full_path)
    os.makedirs(dir_path, exist_ok=True)
    return full_path


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
    # Special case: current_sequence.json should live in legacy directory
    if filename == "current_sequence.json":
        # Get the legacy directory path from the current file location
        legacy_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        base_path = legacy_root
    else:
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
    if getattr(sys, "frozen", False):
        dictionary_path = os.path.join(
            os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "dictionary"
        )
    else:
        # Always use root data/dictionary directory
        dictionary_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "data", "dictionary"
            )
        )

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
