import xmlrpc.client 
import operator
import os

FILE_ROUTE = '\\file_data\\client'

class RPC_Client():
	def __init__(self):
		self.ser_mes = [(8001,300),(8002,200),(8003,280),(8004,150),(8005,100)]
		self.ser_mes = sorted(self.ser_mes,key=operator.itemgetter(1))
		self.index = 0
		self.current_port = self.ser_mes[self.index][0]
		self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
		print("This is client,start!")
		print("Currently connect to server ",str(self.current_port))
		self.route = ''
		self.client()

	def client(self):
		while True:
			print()
			print("-----------------------")
			print('输入help可以得到更多的指令!')
			command = (input(self.route + ">"))
			command = list(command.split(' '))
			if  len(command) == 1 and command[0] == 'help':
				print('ls：列举当前文件夹中的所有文件')
				print('cd route：进入下一级route目录')
				print('mkdir fold_name：创建文件夹')
				print('rmdir fold_name：删除文件夹')
				print('rename old_name new_name：文件夹或文件重命名')
				print('mknod file_name：创建文件')
				print('remove file_name：删除文件')
				print('read file_name：读文件内容')
				print('write file_name content：写文件内容')
				print('open file_name：以可视化形式打开文件，并且可以直接读取和删改')
			
			elif len(command) == 1 and command[0] == 'ls':
				try:
					mes = self.server_proxy.file_ls(self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					print ("目录为: ",mes)

			elif len(command) == 2 and command[0] == 'cd':
				if command[1] == '..':
					if '\\' not in self.route and len(self.route) != 0:
						self.route = ''
					else:
						try:
							index1 = self.route.rindex('\\')
						except:
							print('输入错误！')
						else:
							self.route = self.route[0:index1]
				else:
					try:
						mes = self.server_proxy.file_cd(self.route + '\\' + command[1])
					except:
						print("server",str(self.current_port),"is down")
						self.index = (self.index+1)%5
						self.current_port = self.ser_mes[self.index][0]
						self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
						print("Reconnect to second server",self.current_port)
						print("Please input the command again")
					else:
						if mes == False:
							print('输入的路径不正确！')
						else:
							if self.route == '':
								self.route = command[1]
							else:
								self.route = self.route + '\\' + command[1]

			elif len(command) == 2 and command[0] == 'mkdir':
				try:
					mes = self.server_proxy.file_mkdir(self.route + '\\' + command[1])
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == False:
						print("要创建的文件夹已经存在，不能重复创建！")
					else:
						print("成功创建新文件夹！")

			elif len(command) == 2 and command[0] == 'rmdir':
				try:
					mes = self.server_proxy.file_rmdir(self.route, command[1])
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == 0:
						print("要删除的文件夹不存在，删除失败！")
					elif mes == -1:
						print("当前文件夹不是空的,不可以删除！")
					elif mes == 1:
						print("成功删除指定文件夹！")

			elif len(command) == 3 and command[0] == 'rename':
				try:
					mes = self.server_proxy.file_rename(command[1],command[2],self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == 0:
						print("要重命名的文件或文件夹不存在，重命名失败！")
					elif mes == -1:
						print("新命名的名字已经存在，不能重命名！")
					elif mes == 1:
						print("重命名成功！")

			elif len(command) == 2 and command[0] == 'mknod':
				try:
					mes = self.server_proxy.file_mknod(command[1],self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == False:
						print("要创建的文件已经存在，创建失败！")
					elif mes == True:
						print("创建文件成功！")

			elif len(command) == 2 and command[0] == 'remove':
				try:
					mes = self.server_proxy.file_remove(command[1],self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == 0:
						print("要删除的文件不存在，删除失败！")
					elif mes == -1:
						print("删除的为文件夹，删除失败，需要更换另一个指令！")
					elif mes == 1:
						print("删除文件成功")

			elif len(command) == 2 and command[0] == 'read':
				file_path = os.getcwd()
				file_path = file_path + FILE_ROUTE
				if command[1] in os.listdir(file_path):
					file_path = file_path + '\\' + command[1]
					with open(file_path,'r') as f1:
						data = list(f1.readlines())
					for i in range(len(data)):
						data[i] = data[i][0:-1]
					print('访问的数据已在缓存，文件数据如下：')
					print(data)
				else:
					try:
						mes = self.server_proxy.file_read(command[1],self.route)
					except:
						print("server",str(self.current_port),"is down")
						self.index = (self.index+1)%5
						self.current_port = self.ser_mes[self.index][0]
						self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
						print("Reconnect to second server",self.current_port)
						print("Please input the command again")
					else:
						if mes == None:
							print("输入的文件不存在,读取数据失败!")
						else:
							file_path = file_path + '\\' + command[1]
							with open(file_path,'w') as f1:
								f1.writelines(mes)
							for i in range(len(mes)):
								mes[i] = mes[i][0:-1]
							print("访问数据不在缓存，从服务器下载，缓存到本地，文件数据如下")
							print(mes)

			elif len(command) == 3 and command[0] == 'write':
				file_path = os.getcwd()
				file_path = file_path + FILE_ROUTE
				if command[1] in os.listdir(file_path):
					file_path = file_path + '\\' + command[1]
					with open(file_path,'w') as f1:
						f1.writelines(command[2])
					print("数据已经更新到本地缓存，现在上传到服务器中！")
				try:
					mes = self.server_proxy.file_write(command[1],command[2],self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == False:
						print("输入的文件不存在,写入数据失败!")
					elif mes == True:
						print("数据已经更新到服务器文件！")

			elif len(command) == 2 and command[0] == 'open':
				try:
					mes = self.server_proxy.file_open(command[1],self.route)
				except:
					print("server",str(self.current_port),"is down")
					self.index = (self.index+1)%5
					self.current_port = self.ser_mes[self.index][0]
					self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:"+str(self.current_port))
					print("Reconnect to second server",self.current_port)
					print("Please input the command again")
				else:
					if mes == 0:
						print("输入的文件不存在,读取数据失败!")
					elif mes == 1:
						print('读取或修改数据完成！')

			else:
				print("输入格式错误！")

	

if __name__ == "__main__":
	rpc_client = RPC_Client()



