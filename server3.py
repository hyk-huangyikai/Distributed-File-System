from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import xmlrpc.client 
import threading
import random
import time
import os
import shutil

FILE_ROUTE = "\\file_data\\server\\server3"

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):pass

class MyThread(threading.Thread):
	def __init__(self,threadName,event,port,proxy,manage_data,my_port):
		threading.Thread.__init__(self,name=threadName)
		self.threadEvent = event
		self.port = port
		self.proxy = proxy
		self.manage_data = manage_data
		self.my_port = my_port


	def run(self):
		while True:
			self.threadEvent.wait()
			print('accessing')
			try:
				own_file_path = os.getcwd() + FILE_ROUTE
				self.proxy.file_update(own_file_path,self.my_port)
			except:
				print('down')
				self.threadEvent.clear()
			else:
				self.threadEvent.clear()
				print("Update data to server ",str(self.port))


class ManageData():
	def store_data(self):
		self.server_proxy = None
		self.lock = threading.RLock()    #创建 可重入锁


	def proxy(self,server_proxy,port):
		self.server_proxy = server_proxy
		self.port = port

		self.sinal = threading.Event()
		for i in range(len(self.server_proxy)):
		    t = MyThread(str(i),self.sinal,self.server_proxy[i][0],self.server_proxy[i][1],self,self.port)
		    t.daemon = True
		    t.start()

	def file_update(self,file_route,port):
		print("Update data from server ",port)
		own_file_path = os.getcwd() + FILE_ROUTE
		self.lock.acquire() 
		if 'server3' in os.listdir(os.getcwd() + '\\file_data\\server'):
			shutil.rmtree(own_file_path)
		try:
			shutil.copytree(file_route,own_file_path)
		except:
			self.lock.release()
		else:
			self.lock.release()
			self.sinal.set()
			self.sinal.clear()

	def update(self):
		self.sinal.set()
		self.sinal.clear()

	def file_mkdir(self,folder_name):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE + '\\' + folder_name
		try:
			os.mkdir(file_path)
		except OSError:
			# print("要创建的文件夹已经存在，不能重复创建！")
			return False
		else:
			# print("成功创建新文件夹！")
			self.update()
			return True

	def file_rmdir(self,route,folder_name):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if folder_name not in os.listdir(file_path):
			# print("要删除的文件夹不存在，删除失败！")
			return 0
		else:
			file_path = file_path + '\\' + folder_name
			try:
				os.rmdir(file_path)
			except OSError:
				# print("当前文件夹不是空的,不可以删除！")
				return -1
			else:
				# print("成功删除指定文件夹！")
				self.update()
				return 1

	def file_ls(self,file_route):
		file_path = os.getcwd()
		if len(file_route) != 0:
			file_path = file_path + FILE_ROUTE + '\\' + file_route
		else:
			file_path = file_path + FILE_ROUTE
		return os.listdir(file_path)

	def file_rename(self,old_name,new_name,route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if old_name not in os.listdir(file_path):
			# print("要重命名的文件或文件夹不存在，重命名失败！")
			return 0
		else:
			old_file_path = file_path + '\\' + old_name
			new_file_path = file_path + '\\' + new_name
			try:
				os.rename(old_file_path,new_file_path)
			except OSError:
				# print("新命名的名字已经存在，不能重命名！")
				return -1
			else:
				# print("重命名成功！")
				self.update()
				return 1

	def file_remove(self,file_name,route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if file_name not in os.listdir(file_path):
			# print("要删除的文件不存在，删除失败！")
			return 0
		else:
			file_path = file_path + '\\' + file_name
			try:
				os.remove(file_path)
			except OSError:
				# print("删除的为文件夹，删除失败，需要更换另一个指令！")
				return -1
			else:
				# print("删除文件成功")
				self.update()
				return 1

	def file_mknod(self,file_name,route):
		file_path = os.getcwd()
		if len(route) == 0:
			file_path = file_path + FILE_ROUTE + '\\' + file_name
		else:
			file_path = file_path + FILE_ROUTE + '\\' + route + '\\' + file_name
		try:
			file1 = open(file_path,'w')
			file1.close()
		except:
			# print("要创建的文件已经存在，创建失败！")
			return False
		else:
			# print("创建文件成功！")
			self.update()
			return True

	def file_cd(self,file_route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE + '\\' + file_route
		try:
			os.listdir(file_path)
		except OSError:
			# print("输入的路径不正确！")
			return False
		else:
			return True

	def is_dir(self,fold_name):
		file_path = os.getcwd() + FILE_ROUTE + '\\' + folder_name
		return os.path.is_dir(file_path)

	def is_file(self,file_name):
		file_path = os.getcwd() + FILE_ROUTE + '\\' + file_name
		return os.path.is_dir(file_path)

	def file_read(self,file_name,route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if file_name not in os.listdir(file_path):
			# print("输入的文件不存在！读取数据失败")
			return None
		else:
			file_path = file_path + '\\' + file_name
			f1 = open(file_path,'r')
			#文件锁上锁
			self.lock.acquire()  
			data = list(f1.readlines())
			#文件锁解锁
			self.lock.release()
			f1.close()

			return data

	def file_write(self,file_name,content,route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if file_name not in os.listdir(file_path):
			# print("输入的文件不存在！写入数据失败")
			return False
		else:
			file_path = file_path + '\\' + file_name
			f1 = open(file_path,'w')
			#文件锁上锁
			self.lock.acquire()  
			f1.writelines(content)
			#文件锁解锁
			self.lock.release()
			# print('数据已经写入文件！')
			self.update()
			return True

	def file_open(self,file_name,route):
		file_path = os.getcwd()
		file_path = file_path + FILE_ROUTE
		if len(route) != 0:
			file_path = file_path + '\\' + route
		if file_name not in os.listdir(file_path):
			# print("输入的文件不存在！读取数据失败")
			return 0
		else:
			file_path = file_path + '\\' + file_name
			os.popen(file_path).read()
			self.update()
			return 1

class Server():

	def __init__(self,port):
		self.port = port
 

	def build_server(self):
		server = ThreadXMLRPCServer(("localhost", self.port), allow_none=True)
		print ("This is Server ",self.port,"start!")
		self.manage_data = ManageData()
		self.manage_data.store_data()
		self.connect_to_other_server()

		server.register_instance(self.manage_data)
		print()
		server.serve_forever()

	def connect_to_other_server(self):
		self.server_port = [8001]
		self.server_proxy = []
		for port in self.server_port:		
			proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(port))
			self.server_proxy.append((port,proxy))
			print("Connected to server ",str(port))
			self.manage_data.proxy(self.server_proxy,self.port)


if __name__ == "__main__":
	rpc_server = Server(8003)
	rpc_server.build_server()
