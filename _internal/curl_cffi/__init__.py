"""""" # start delvewheel patch
def _delvewheel_patch_1_5_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'curl_cffi.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-curl_cffi-0.5.10b4')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-curl_cffi-0.5.10b4')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not ctypes.windll.kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError()))


_delvewheel_patch_1_5_1()
del _delvewheel_patch_1_5_1
# end delvewheel patch

__all__ = [
    "Curl",
    "CurlInfo",
    "CurlOpt",
    "CurlMOpt",
    "CurlECode",
    "CurlHttpVersion",
    "CurlError",
    "AsyncCurl",
    "ffi",
    "lib",
]

# This line includes _wrapper.so into the wheel
from ._wrapper import ffi, lib

from .const import CurlInfo, CurlMOpt, CurlOpt, CurlECode, CurlHttpVersion
from .curl import Curl, CurlError
from .aio import AsyncCurl
