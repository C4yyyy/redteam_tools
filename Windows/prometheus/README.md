<h1>Prometheus usage </h1>

#Change prometheus IP to your local IP (changing the port is optional) \n
#Run the following command and it will be compilen in .exe file\n

````bash
g++/i686-w64-mingw32-g++ prometheus.cpp -o prometheus.exe -lws2_32 -s -ffunction-sections -fdata-sections -Wno-write-strings -fno-exceptions -fmerge-all-constants static-libstdc++ -static-libgcc
````
