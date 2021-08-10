import salt.modules.win_wua
import winreg
import time


#importa informacion del registro

def get_registry_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(winreg, path[0])
        return get_registry_value(path[1:], name, start_key)
    else:
        subkey =path.pop(0)
    with winreg.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return get_registry_value(path, name, handle)
        
        else:
            desc, i = None, 0
            while not desc or desc[0] !=name:
                desc = winreg.EnumValue(handle, i)
                i +=1 
            return desc [1]
try:
    WSUSSER = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", "UseWUServer")
    if WSUSSER == 1:
        wsusip = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate", "WUServer") 
        print ('El servidor esta conectado a WSUS:' , wsusip)
        time.sleep(10)
        salt.modules.win_wua.list(categories=["Security Updates"], summary=True, install=True)        
except OSError as err:
    print ('El servidor no tiene wsus y esta conectado a intenet')
    print ('Se procede a instalar parches directo desde internet')
    time.sleep(5)
    salt.modules.win_wua.list(categories=["Security Updates"], summary=True, install=True)

    







