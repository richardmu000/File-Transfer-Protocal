import socket
import sys
import os
import subprocess
from subprocess import Popen, PIPE


def Main():
	port = 12397

	s = socket.socket()
	#s.bind((host,port))
	s.bind(('', port))

	print("server started")
	s.listen(1)

	

	c, addr = s.accept()
	print("client connected ip:<"+str(addr)+">")
	#name = c.recv(1024).decode()
	#print("client name: "+name)
	#command = "ls -la"
	#command = command.split()
	#p = Popen(['ls'], stdout=PIPE)
	#result = p.communicate()
	#c.send(result[0])
	p = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
	result = p.communicate()
	mssg = "FOLDERS:------------\n"+result[0].decode()
	p = subprocess.Popen('ls -p | grep -v /', shell=True, stdout=subprocess.PIPE)
	result = p.communicate()
	mssg = mssg + "\nFILES:------------\n"+result[0].decode()
	
	#c.send(b'connected')
	#c.send(mssg.encode())
	
	while True:
		data = c.recv(1024).decode()
		if data == "list content":
			c.send(mssg.encode())
			print("content list sent")
			s.listen(1)
			c, addr = s.accept()
		elif data == "connection":
			c.send(b'connection established')
			s.listen(1)
			c, addr = s.accept()
		elif data[:13] == "folder viewed":
			foldername = data[15:]
			#print(data)
			#print(foldername)
			if os.path.isdir(foldername):
				p = Popen(['ls', foldername], stdout=PIPE)
				result = p.communicate()
				c.send(result[0])
				print("folder content sent")
				s.listen(1)
				c, addr = s.accept()
			else:
				print("requested folder does not exist")
				c.send(b"folder does not exist")
				s.listen(1)
				c, addr = s.accept()
		elif os.path.isfile(data):
			print("download requested for "+data)
			msg = "EXISTS "+str(os.path.getsize(data))
			c.send(msg.encode())
			userResponse = c.recv(1024)
			if userResponse[:2] == b'OK':
				with open(data, 'rb') as f:
					bytesToSend = f.read(1024)
					c.send(bytesToSend)
					while bytesToSend != b'':
						bytesToSend = f.read(1024)
						c.send(bytesToSend)
					print("completed")
					s.listen(1)
					c, addr = s.accept()
			else:
				print("download canceled")
				c.send(b"download canceled")
		elif data[:7] == "message":
			print("from "+name+": "+str(data))
			data = input(' -> ')
			c.send(data.encode())
		elif data == "client quit":
			print("client quit")
			closeserver = input("close server?")
			if closeserver == "yes":
				break
			else:
				#c.close()
				s.listen(1)
				c, addr = s.accept()
				
				print("client connected ip:<"+str(addr)+">")
				#name = c.recv(1024).decode()
				#print("client name: "+name)
				
				p = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
				result = p.communicate()
				mssg = "FOLDERS:------------\n"+result[0].decode()
				p = subprocess.Popen('ls -p | grep -v /', shell=True, stdout=subprocess.PIPE)
				result = p.communicate()
				mssg = mssg + "\nFILES:------------\n"+result[0].decode()
				#c.send(mssg.encode())
				#c.send(b'connected')
			
		else:
			print("requested file or folder does not exist")
			c.send(b"file or folder does not exist")
			s.listen(1)
			c, addr = s.accept()
	
	s.close()
		


if __name__ == '__main__':
	Main()
		
		

		
