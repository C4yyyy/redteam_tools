#!/bin/bash

#Para eliminar montura:
#umount /mnt
#---------------------
#Crear montura con credenciales anonimas:
# |
# V
#mount -t cifs '10.10.10.103/Department Shares'
#---------------------------------------------
#Crear montura con credenciales de un dominio
# |
# V
#sudo mount -t cifs -o username=prueba,pass=pru3ba,domain=prueba.local //IP/Recurso /mnt/
#----------------------------------------------------------------------------------------
#ejecutar en el directorio donde se ha hecho la montura de samba
#POC
#pwd
# $ /mnt/smbmounted
#bash /home/user/Desktop/script.sh

#for i in $(find . -maxdepth 1 -type d); do mkdir -v $i/wepale 2>/dev/null && rm -r $i/wepale && echo -e "\n [*] El directorio $i tiene permiso de escritura. \n";done | grep -v "se ha creado el directorio" | tr -d './'

for i in $(find . -type d); do
	touch $i/c4yyyy 2>/dev/null && echo -e "$i - Archivo Creado" && rm -r $i/c4yyyy
	mkdir $i/c4yyyy 2>/dev/null && echo -e "$i - Directorio Creado" && rmdir $i/c4yyyy
done
