import glob
import os
import vdf
import winreg
import send2trash
from collections.abc import Mapping


def showError(errorIndex, error, *errorDetails):
    print('[ERROR]', error)
    for errorDetail in errorDetails:
        print('[ERRORINFO]', errorDetail)
    os.system("pause")

    if errorIndex > 0:
        exit(errorIndex)


def showInfo(*infos):
    for info in infos:
        print('[INFO]', info)


steamLibraryPath = []

try:
    steamRegistryKey = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        "SOFTWARE\\WOW6432Node\\Valve\\Steam"
        )
except OSError:
    try:
        steamRegistryKey = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Valve\\Steam"
            )
    except OSError as e:
        showError(1, 'Steam Registry Error', str(e))
    else:
        showInfo('32-bit detected')
else:
    showInfo('64-bit detected')


try:
    steamQuery = winreg.QueryValueEx(steamRegistryKey, "InstallPath")

    if not isinstance(steamQuery[0], str):
        raise ValueError('value is NOT string')

    if steamQuery[1] == winreg.REG_EXPAND_SZ:
        steamPath = os.path.expandvars(steamQuery[0])
    else:
        steamPath = steamQuery[0]

except OSError as e:
    showError(2, 'Registry Value Not Found', str(e))

except ValueError as e:
    showError(2, 'Registry Value Error', str(e))

finally:
    winreg.CloseKey(steamRegistryKey)

listPath = os.path.join(steamPath, 'steamapps\\libraryfolders.vdf')
showInfo('Library Folders List Path:', listPath)

if os.path.exists(listPath):
    showInfo(f'Library Folders List Found: {listPath}')
else:
    showInfo('Library Folders List Not Found')


try:
    with open(listPath, 'r') as file:
        listDict = vdf.load(file)
except NameError:
    pass
except OSError as e:
    showError(3, 'KeyValues File Error', str(e))
except SyntaxError as e:
    showError(3, 'KeyValues to Dict Conversion Failed', str(e))
else:
    showInfo('KeyValues to Dict Conversion Succeeded')

steamLibraryPath.append(steamPath)
showInfo(f'Library added: {steamPath}')

if 'libraryfolders' in listDict:
    libraryFolders = listDict['libraryfolders']
elif 'LibraryFolders' in listDict:
    libraryFolders = listDict['LibraryFolders']
elif len(listDict) != 0:
    libraryFolders = listDict[listDict.keys()[0]]
else:
    showError(4, 'KeyValues to Dict Conversion Failed', listDict)


try:
    for key, value in libraryFolders.items():
        if (isinstance(value, Mapping) and
            'path' in value and
            isinstance(value["path"], str)):
            installPath = value["path"]
        elif isinstance(value, str):
            installPath = value
        else:
            continue

        if os.path.isdir(installPath):
            steamLibraryPath.append(installPath)
            showInfo(f'Library added: {installPath}')

except NameError:
    pass

except (KeyError, TypeError) as e:
    showInfo('Library Dict Failed', str(e))


for path in steamLibraryPath:
    path = os.path.join(path, 'steamapps\\common\\Team Fortress 2\\tf\\')

    if not os.path.exists(path):
        showInfo(f'directory not found: {path}')
        continue

    showInfo(f'directory found: {path}')
    for file in glob.iglob(os.path.join(path, '**.cache')):
        send2trash.send2trash(file)
        showInfo(f'file sended to recycle bin: {file}')


showInfo('Removal finished')
os.system("pause")
