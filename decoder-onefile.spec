# -*- mode: python ; coding: utf-8 -*-

import pathlib

from threadpoolctl import threadpool_info

block_cipher = None


def get_ext_path():
    x = threadpool_info()
    if not x:
        return []
    x = x[0].get('filepath')
    if not x:
        return []
    print('FOUND:', x)
    return [str(pathlib.Path(x).parent)]


a = Analysis(
    ['SatsDecoder/__main__.py'],
    pathex=get_ext_path(),
    binaries=[],
    datas=[('res/*.png', 'res')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SatsDecoder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res/icon.png'],
)
