import socket
import threading
import sqlite3
from cfg import *
import sys
import time
from database import getallkeys, getkeyactivity, setkeyactivity, clearactivity


class Server:
	def __init__(self,ip,port):
		self.connections = []
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.ip,self.port))
		self.s.listen(0)
		threading.Thread(target=self.connect_handler).start()
		print(f'Сервер запущен на {ip}:{port}')

	def connect_handler(self):
		while True:
			client, address = self.s.accept()
			self.connections.append(client)
			thread = ClientThread(client)
			thread.start()
			time.sleep(1)

class ClientThread(threading.Thread, Server):
	def __init__(self,args):
		threading.Thread.__init__(self,args=((args,)))
		self.client = args
		self.alive = True
		self.address = self.client.getpeername()[0]
		self.key = ""
		self.once = True
		self.keys = getallkeys()

	def run(self):
		while True:
			try:
				key = self.client.recv(1024).decode()
				if key != b'':
					if key in self.keys and getkeyactivity(key)<=1:
						self.key = key
						if self.once:
							setkeyactivity(key,getkeyactivity(key)+1)
							self.once = False
						self.client.send("1".encode())
					else:
						self.client.send("0".encode())
					
			except ConnectionResetError:
				self.alive = False
				self.once = False
				setkeyactivity(key,getkeyactivity(key)-1)
				sys.exit(0)

			except Exception as e:
				with open("ClientThreadCrash.txt","a") as file:
					file.write(str(e)+"\n")

clearactivity()
server = Server(server_ip,server_port)