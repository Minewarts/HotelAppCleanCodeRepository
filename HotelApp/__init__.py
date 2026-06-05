import os

# Make imports like `import HotelApp.services` resolve to the code in `src/HotelApp`
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_src_pkg = os.path.join(_root, 'src', 'HotelApp')
if os.path.isdir(_src_pkg):
    __path__.insert(0, _src_pkg)
