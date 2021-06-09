import socket
import threading
import sqlite3
import json
from cfg import *
import sys
import time
from database import getallkeys, getkeyactivity, setkeyactivity, clearactivity
import traceback


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
		self.once = True
		self.key = ""
		self.version = ""
		self.keys = getallkeys()
		self.errors = 0
		self.data_to_send = {
			"message":"",
			"access":False
		}

	def run(self):
		while True:
			try:
				received_data = json.loads(self.client.recv(1024).decode())
				print(received_data)
				self.key = received_data["key"]
				self.version= received_data["version"]
				self.handle_data()
				self.client.send(json.dumps(self.data_to_send).encode())
					
			except ConnectionResetError:
				self.alive = False
				self.once = False
				if getkeyactivity(self.key)>0 and self.data_to_send["access"]: # нужно будет добавить переменную access
					setkeyactivity(self.key,getkeyactivity(self.key)-1)
				sys.exit(0)

			except Exception as e:
				if self.errors<9:
					print(traceback.format_exc())
					self.errors+=1
				else:
					sys.exit(0)

	def handle_data(self):
		if self.key in self.keys and getkeyactivity(self.key)<=1:
			self.data_to_send.update({"message":"authorized","access":True})
			if self.version != version:
				self.data_to_send.update({"message":"old version","access":False})
			elif self.once:
				setkeyactivity(self.key,getkeyactivity(self.key)+1)
				self.once=False
		else:
			self.data_to_send.update({"message":"wrong key","access":False})

clearactivity()
server = Server(server_ip,server_port)