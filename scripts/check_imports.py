import sys, os
print('cwd:', os.getcwd())
print('sys.path[:5]=', sys.path[:5])
try:
    import HotelApp.services as mod
    print('Imported HotelApp.services ->', mod)
    print('dir contains:', [n for n in dir(mod) if 'User' in n or 'user' in n])
except Exception as e:
    print('Import Error HotelApp.services:', type(e), e)

try:
    import src.HotelApp.services as mod2
    print('Imported src.HotelApp.services ->', mod2)
    print('dir2 contains:', [n for n in dir(mod2) if 'User' in n or 'user' in n])
except Exception as e:
    print('Import Error src.HotelApp.services:', type(e), e)

print('\nPython executable:', sys.executable)
print('Python version:', sys.version)
