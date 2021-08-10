import winreg
import time
import os

r = 1
while (r == 1):
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
        reinicio = get_registry_value(r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired", "RebootRequiredNotificationFlags")
        r = reinicio
        if reinicio == 0:
            print ('El Servidor necesita ser reiniciado:' ,reinicio)
            time.sleep(10)
            os.system('shutdown /r /t 0')
    except OSError as err:
        print ('El Servidor no necesita ser reiniciado')
        time.sleep(5)
        
        
        




