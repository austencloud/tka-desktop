from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import sys
import os

# Get the project directory (where the spec file is)
project_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
src_dir = os.path.join(project_dir, "src")

# Define data files to include
datas = [
    (os.path.join(project_dir, "settings.ini"), "."),
    (src_dir, "src"),
    # Make sure profiler is included (appears to be at src root level)
    (os.path.join(src_dir, "profiler.py"), ".")
]

a = Analysis(
    [os.path.join(project_dir, 'launcher.py')],  # Use our launcher script
    pathex=[project_dir, src_dir],  # Include both directories in search path
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'main_window',
        'main_window.main_window',
        'utils',
        'settings_manager',
        'splash_screen'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TheKineticConstructor v0.2',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KineticConstructor',
)