import os
import winreg
import kv2dict
from send2trash import send2trash

steamLibraryPath = []

try:
    steamRegistry = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
except:
    try:
        steamRegistry = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Valve\Steam")
    except:
        print('[ERROR] steam registry not found (maybe steam is not installed)')
        os.system("pause")
        exit(1)
    else:
        print('[INFO] 32-bit detected')
else:
    print('[INFO] 64-bit detected')

try:
    steamPath = winreg.QueryValueEx(steamRegistry, "InstallPath")[0]
    assert isinstance(steamPath, str)
except:
    print('[ERROR] registry value not found')
    os.system("pause")
    exit(2)

libraryListingPath = os.path.join(steamPath, 'steamapps\\libraryfolders.vdf')
print(f'[INFO] Library Listing found: {libraryListingPath}')

try:
    with open(libraryListingPath, 'r')  as libraryListingKeyvalues:
        libraryListingDict = kv2dict.kvFile2Dict(libraryListingKeyvalues)
except:
    print('[ERROR] keyvalues to dict conversion failed')
    os.system("pause")
    exit(3)
else:
    print('[INFO] keyvalues to dict conversion succeeded')

steamLibraryPath.append(steamPath)
print(f'[INFO] Library added: {steamPath}')

try:
    it = 1
    while str(it) in libraryListingDict['libraryfolders']:
        steamLibraryPath.append(libraryListingDict['libraryfolders'][str(it)]['path'])
        print(f'[INFO] Library added: {libraryListingDict["libraryfolders"][str(it)]["path"]}')

        it += 1
except:
    print('[ERROR] library listing keyvalues is invalid')
    os.system("pause")
    exit(4)

for path in steamLibraryPath:
    path = os.path.join(path, 'steamapps\\common\\Team Fortress 2\\tf\\')
    print(f'[INFO] looking for directory: {path}')
    if(os.path.exists(path)):
        for file in [f for f in os.listdir(path) if os.path.splitext(f)[1] == '.cache']:
            file = os.path.join(path, file)
            send2trash(file)
            print(f'[INFO] file sended to recycle bin: {file}')

os.system("pause")

