import socket
import json
from threading import Thread
import time


class client(Thread):
	def __init__(self,server_ip,server_port,key,version):
		Thread.__init__(self)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.key = key
		self.version = version
		self.server_ip = server_ip
		self.server_port = server_port
		self.access = False
		self.data = {
			"key":self.key,
			"version":self.version
		}
		self.message = "connecting..."
		self.s.connect((server_ip, server_port))

	def run(self):
		self.checker()

	def checker(self):
		while True:
			self.s.send(json.dumps(self.data).encode())
			data = json.loads((self.s.recv(1024)).decode())
			#print(data)
			time.sleep(1)
			self.access = data["access"]
			self.message = data["message"]

	def get_access(self):
		return self.access


if __name__ == "__main__":
	from cfg import *

	#load config
	with open("config.json",encoding ="UTF-8") as jsonFile:
		config = json.load(jsonFile)



	cl = client(server_ip,server_port,config["key"],version)
	cl.start()
	while True:
		time.sleep(1)
		print(cl.get_access())
		print(cl.message)