import salt.modules.win_wua
import salt.modules.win_wusa
import os
import platform
import socket
import time
import winreg

#rescata informacion de Update disponibles en servidor via saltstack
disponibles = salt.modules.win_wua.available(categories=["Security Updates"], severities=["Critical"])
print (disponibles)

instalados = salt.modules.win_wua.list(categories=["Security Updates"], summary=True)
print (instalados)

#Variables de obtencion datos del sistema operativo

sistema = platform.platform(terse=True)
hostname = socket.gethostname()
ip_address1 = socket.gethostbyname(hostname)
ahora = time.strftime("%c")

#crea archivo de parches instalados 

os.system('wmic qfe get Description,hotfixid,installedon /format:texttablewsys > "c:\python\Listado_de_Parches_Antes.txt"')

archivo4 = open('C:\Python\Listado_de_Parches_Antes.txt', mode="r")
texto3 = archivo4.read()
archivo4.close()

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
Detect = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Detect", "LastSuccessTime")
Download = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Download", "LastSuccessTime")
Install = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Install", "LastSuccessTime")


#crea archivo de informe del equipo

archivo = open("C:\Python\Informe_parchado_Primario.txt", "w")
archivo.write('I N F O R M A C I O N   G E N E R A L   D E L   E Q U I P O\n')
archivo.write("----------------------------------------------------------- \n")
archivo.write(" \n")
archivo.write("Nombre del Sistema Operativo  :{}".format(sistema))
archivo.write(" \n")
archivo.write("Nombre del Equipo             :%s" % hostname)
archivo.write(" \n")
archivo.write('Direccion Ip del Equipo       :%s' % ip_address1)
archivo.write(" \n")
archivo.write("Fecha y hora del Equipo       :%s" % ahora )
archivo.write(" \n")
archivo.write(" \n")
archivo.write("W I N D O W S   U P D A T E   R E S U M E N  \n")
archivo.write("-------------------------------------------- \n")
archivo.write(" \n")
archivo.write(" \n")
archivo.write("Most recent check for Update :%s" % Detect)
archivo.write(" \n")
archivo.write("Update were Installed        :%s" % Download)
archivo.write(" \n")
archivo.write("Most recent successful Update:%s" % Install)
archivo.write(" \n")
archivo.write(" \n")
archivo.write(" \n")
archivo.write("I N F O R M E   D E   P A R C H A D O  \n")
archivo.write("------------------------------------- \n")
archivo.write(" \n")
archivo.write("P A R C H E S   D I S P O N I B L E S  S U M M A R Y \n")
archivo.write("---------------------------------------------------- \n")
archivo.write(" \n")
archivo.write("%s"%instalados)
archivo.write(" \n")
archivo.write(" \n")
archivo.write("D E T A L L E   P A R C H E S   D I S P O N I B L E S   P A R A   S E R   I N S T A L A D O S  \n")
archivo.write("---------------------------------------------------------------------------------------------- \n")
archivo.write(" \n")
archivo.write("%s"%disponibles)
archivo.write(" \n")
archivo.write(" \n")
archivo.write("L I S T A D O   D E   P A R C H E S   E N   E L   S I S T E M A  \n")
archivo.write("---------------------------------------------------------------- \n")
archivo.write(" \n")
archivo.write("%s"%texto3)

print ('Proceso Terminado')

