from pythonping import ping
from sys import *
from signal import signal, SIGINT

#Created by C4yyyy

def handler(signal_reveived, frame):
	print('\n [!] Saliendo...\n')
	exit(0)


for i in range(255):

	response_list = ping("10.10.10." + str(i), count=1) #Edit ip

	if response_list.rtt_avg_ms < 300:
		print("10.10.10.{} --> Host up".format(i)) #Edit ip
	else:
		print("10.10.10.{} --> Host down".format(i)) # Edit ip

	signal(SIGINT,handler)
