# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files

# Project Name
project_name = "The Kinetic Constructor"

# Ensure all data and assets are included
data_files = collect_data_files("src/data", includes=["*.csv", "*.json"])
image_files = collect_data_files("src/images")
dictionary_files = collect_data_files("src/generated_data/dictionary")
temp_files = collect_data_files("src/temp")

# PyInstaller Analysis
a = Analysis(
    ["src/main.py"],  # Entry point
    pathex=["."],
    binaries=[],
    datas=[
        ("settings.ini", "."),
        *data_files,
        *image_files,
        *dictionary_files,
        *temp_files
    ],
    hiddenimports=[
        "src.main_window.main_widget.json_manager.json_manager",
        "src.settings_manager.global_settings.app_context"
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

# PyInstaller Build
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=project_name,
    debug=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you need console output
    icon=None
)
