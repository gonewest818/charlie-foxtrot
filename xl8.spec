# -*- mode: python ; coding: utf-8 -*-

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('config.ini')

block_cipher = None

added_files = [
   ('config.ini', '.'),
   ('xl8_dialog.ui', '.'),
   ('xl8.svg', '.')
]

a = Analysis(
    ['xl8.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='xl8',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=os.getenv('CODESIGN_ID'),
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='xl8',
)
app = BUNDLE(
   coll,
   name='xl8.app',
   #icon='xl8_icon.png',
   bundle_identifier='io.github.gonewest818.xl8',
   info_plist={
       'CFBundleShortVersionString': cfg['xl8']['APP_VERSION'],
       'LSUIElement': True
   }
)
