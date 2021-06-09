import socket


class client:
	def __init__(self,server_ip,server_port,key):
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.key = key
		self.server_ip = server_ip
		self.server_port = server_port
		self.s.connect((host, port))
	def checker(self):
		while True:
			s.send(key.encode())
			data = s.recv(1024)