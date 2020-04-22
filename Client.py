import socket

class Client():

	def __init__(self, addr, port):

		self.addr = addr
		self.port = port
		self.conn = None

	def run(self):

		self.conn = self.connect()

	def connect(self):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		print(f"Connecting to {self.addr}:{self.port}")
		s.connect((self.addr, self.port))

		s.sendall(b"Hello")
		msg = s.recv(1024)

		if msg.decode("utf-8") == "Hello":
			print("Connection established")

		return s

	def send(self, payload):

		self.conn.sendall(bytes(payload, 'utf-8'))

	def recv(self):

		return self.conn.recv(1024).decode('utf-8')



if __name__ == "__main__":
	
	c = Client("localhost", 8080)    
	c.connect()