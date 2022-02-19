# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

excludes = [
    '_abc',
    '_ast',
    '_collections',
    '_compat_pickle',
    '_ctypes',
    '_frozen_importlib',
    '_frozen_importlib_external',
    '_functools',
    '_heapq',
    '_imp',
    '_io',
    '_locale',
    '_opcode',
    '_operator',
    '_pickle',
    '_signal',
    '_sre',
    '_stat',
    '_struct',
    '_thread',
    '_warnings',
    '_weakref',
    '_winapi',
    'ast',
    'atexit',
    'builtins',
    'ctypes',
    'ctypes._endian',
    'dis',
    'errno',
    'importlib',
    'importlib._bootstrap',
    'importlib._bootstrap_external',
    'importlib.abc',
    'importlib.machinery',
    'importlib.util',
    'inspect',
    'itertools',
    'linecache',
    'marshal',
    'math',
    'msvcrt',
    'multiprocessing',
    'multiprocessing.context',
    'multiprocessing.popen_spawn_win32',
    'multiprocessing.process',
    'multiprocessing.reduction',
    'multiprocessing.spawn',
    'multiprocessing.util',
    'nt',
    'opcode',
    'os.path',
    'pickle',
    'pkgutil',
    'pyimod01_os_path',
    'pyimod02_archive',
    'pyimod03_importers',
    'pyimod04_ctypes',
    'runpy',
    'signal',
    'struct',
    'subprocess',
    'sys',
    'threading',
    'time',
    'token',
    'tokenize',
    'typing',
    'typing.io',
    'typing.re',
    'winreg',
    'zipimport',
    'zlib'
]

a = Analysis(['token-grabber.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=excludes,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.exclude_system_libraries()
excluded_binaries = [
    'VCRUNTIME140.dll',
    'msvcp140.dll',
    'mfc140u.dll']
a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_binaries])

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Lunar Client Timer Addon',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon="C:/Users/willi/Downloads/lunar_logo.ico")