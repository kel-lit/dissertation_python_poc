import socket

class Server():

	def __init__(self, host, port):

		self.host = host
		self.port = port
		self.conn = None

	def run(self):
		
		self.conn = self.setup()
		

	def setup(self):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		s.bind((self.host, self.port))
		s.listen()

		conn, addr = s.accept()

		print(f"Incoming connection from {addr[0]}:{addr[1]}")
		while True:
			
			msg = conn.recv(1024)
			
			if msg.decode("utf-8") == "Hello":
				conn.sendall(b"Hello")
				break

			print(msg.decode("utf-8"))

		print("Connection established")
		return conn

	def send(self, payload):

		self.conn.sendall(bytes(payload, 'utf-8'))
	
	def recv(self):

		return self.conn.recv(1024).decode('utf-8')
		
		

if __name__ == "__main__":
	
	s = Server("localhost", 8080)
	s.run()