import os
import winreg
import kv2dict
from send2trash import send2trash

steamLibraryPath = []

try:
    steamRegistryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
except OSError:
    try:
        steamRegistryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Valve\Steam")
    except OSError as e:
        print('[ERROR] Steam Registry Error (maybe steam is not installed)')
        print('[ERRORINFO]', str(e))
        os.system("pause")
        exit(1)
    else:
        print('[INFO] 32-bit detected')
else:
    print('[INFO] 64-bit detected')


try:
    steamQuery = winreg.QueryValueEx(steamRegistryKey, "InstallPath")

    if not isinstance(steamQuery[0], str):
        raise ValueError('value is NOT string')
    
    if steamQuery[1] == winreg.REG_EXPAND_SZ:
        steamPath = os.path.expandvars(steamQuery[0])
    else:
        steamPath = steamQuery[0]

except OSError as e:
    print('[ERROR] Registry Value Not Found')
    print('[ERRORINFO]', str(e))
    os.system("pause")
    exit(2)

except ValueError as e:
    print('[ERROR] Registry Value Error')
    print('[ERRORINFO]', str(e))
    os.system("pause")
    exit(2)

finally:
    winreg.CloseKey(steamRegistryKey)


libraryListingPath = os.path.join(steamPath, 'steamapps\\libraryfolders.vdf')

if os.path.exists(libraryListingPath):
    print(f'[INFO] Library Listing Found: {libraryListingPath}')
else:
    print(f'[INFO] Library Listing Not Found')


try:
    with open(libraryListingPath, 'r') as libraryListingKeyvalues:
        libraryListingDict = kv2dict.kvFile2Dict(libraryListingKeyvalues)
except NameError:
    pass
except OSError:
    print('[ERROR] KeyValues File Error')
    print('[ERRORINFO]', str(e))
    os.system("pause")
    exit(3)
except ValueError:
    print('[ERROR] KeyValues to Dict Conversion Failed')
    print('[ERRORINFO]', str(e))
    os.system("pause")
    exit(3)  
else:
    print('[INFO] KeyValues to Dict Conversion Succeeded')

steamLibraryPath.append(steamPath)
print(f'[INFO] Library added: {steamPath}')

try:
    libraryFolders = libraryListingDict['libraryfolders']
except KeyError:
    try:
        libraryFolders = libraryListingDict['LibraryFolders']
    except KeyError:
        print('[ERROR] KeyValues to Dict Conversion Failed')
        print('[ERRORINFO]', libraryListingDict)
        os.system("pause")
        exit(4)

try:
    for it in (i for i in libraryFolders if i.isdecimal()):
        if 'path' in it and isinstance(it["path"], str) and os.path.isdir(it["path"]):
            steamLibraryPath.append(it["path"])
            print(f'[INFO] Library added: {it["path"]}')
        elif isinstance(it, str) and os.path.isdir(it):
            steamLibraryPath.append(it)
            print(f'[INFO] Library added: {it}')

except NameError:
    pass

except (KeyError, TypeError) as e:
    print('[INFO] Library Dict Failed')
    print('[INFO]', str(e))


for path in steamLibraryPath:
    path = os.path.join(path, 'steamapps\\common\\Team Fortress 2\\tf\\')
    print(f'[INFO] looking for directory: {path}')
    if(os.path.exists(path)):
        for file in [f for f in os.listdir(path) if os.path.splitext(f)[1] == '.cache']:
            file = os.path.join(path, file)
            send2trash(file)
            print(f'[INFO] file sended to recycle bin: {file}')


print('[INFO] Removal finished')
os.system("pause")

