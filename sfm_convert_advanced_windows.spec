# -*- mode: python ; coding: utf-8 -*-
# Build command (run on Windows):
#   pyinstaller sfm_convert_advanced_windows.spec

from PyInstaller.utils.hooks import collect_all

tk_datas, tk_binaries, tk_hiddenimports = collect_all('tkinter')

a = Analysis(
    ['sfm_convert_advanced_gui.py'],
    pathex=[],
    binaries=tk_binaries,
    datas=tk_datas,
    hiddenimports=tk_hiddenimports + ['_tkinter', 'xml.etree.ElementTree', 'csv'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sfm_convert_advanced',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,           # replace with 'myicon.ico' if desired
)
