"""
Robust shim to expose `HotelApp.services` symbols for documentation tools.

Problems this solves:
- The project uses a `src/` layout, so importing the package directly
  inside tooling can fail due to relative imports inside package files.
- Loading the package `__init__.py` under a different module name breaks
  relative imports in that file.

Solution:
- Load the concrete module files that define the relevant classes and
  re-export their public names into this shim's globals. This avoids
  executing package-relative imports and makes `HotelApp.services.UserServices`
  importable by tools like mkdocstrings/Griffe.
"""

import importlib.util
import os

_here = os.path.dirname(__file__)
_src_services_dir = os.path.abspath(os.path.join(_here, '..', 'src', 'HotelApp', 'services'))

_candidates = [
    ('user_services.py', ['UserServices']),
    ('hotel_service.py', ['HotelService']),
]

for filename, names in _candidates:
    path = os.path.join(_src_services_dir, filename)
    if not os.path.exists(path):
        continue
    try:
        spec = importlib.util.spec_from_file_location(f'__hotelapp_services_{filename}', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name in names:
            if hasattr(mod, name):
                globals()[name] = getattr(mod, name)
    except Exception:
        # If any load fails, skip gracefully; tooling will report the
        # remaining import errors during doc build.
        pass

__all__ = [
    name for _, names in _candidates for name in names
]
