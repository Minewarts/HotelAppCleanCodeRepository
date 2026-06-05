import sys, os
print('cwd=', os.getcwd())
print('sys.path[0]=', sys.path[0])
print('dir listing root:', sorted([p for p in os.listdir('.') if not p.startswith('.')]) )
try:
    import HotelApp.services as hs
    print('Imported HotelApp.services OK, has UserServices=', hasattr(hs, 'UserServices'))
    print('attrs sample:', [a for a in dir(hs) if 'User' in a or 'Hotel' in a][:30])
except Exception as e:
    print('Import HotelApp.services failed:', type(e), e)

try:
    import src.HotelApp.services as ss
    print('Imported src.HotelApp.services OK, has UserServices=', hasattr(ss, 'UserServices'))
    print('attrs sample src:', [a for a in dir(ss) if 'User' in a or 'Hotel' in a][:30])
except Exception as e:
    print('Import src.HotelApp.services failed:', type(e), e)
