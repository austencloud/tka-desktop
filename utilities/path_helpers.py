import sys
import os
import winreg


def get_images_and_data_path(filename) -> str:
    """This is used for resources like data and images."""
    if hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(".")
    return os.path.join(base_dir, filename)


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
    if getattr(sys, "frozen", False):
        dictionary_path = os.path.join(
            os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "browse"
        )
    else:
        dictionary_path = os.path.join(os.getcwd(), "browse")
    os.makedirs(dictionary_path, exist_ok=True)
    return dictionary_path


def get_win32_special_folder_path(folder_name) -> str:
    """
    Returns the path to the user's custom folder on Windows.
    This folder is set by the user via the Explorer.
    """
    if sys.platform == "win32":
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            ) as key:
                folder_dir, _ = winreg.QueryValueEx(key, folder_name)
                folder_dir = os.path.expandvars(folder_dir)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find the {folder_name} path in the registry."
            ) from e
    else:
        raise NotImplementedError("This function is implemented for Windows only.")

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
