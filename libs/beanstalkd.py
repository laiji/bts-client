import socket

class Beanstalk:
	def put(self,datas):
		try:
			if(len(datas) < 2 and datas[1]!=""):
				raise Exception("Content is empty")
			pri = 1024
			if(len(datas) > 2 and datas[2]):
				pri = int(datas[2])
			delay = 0
			if(len(datas) > 3 and datas[3]):
				delay = int(datas[3])
			content = datas[1]
			timeout = 30
			datas = self.cliSend("put %d %d %d %d\r\n%s"%(pri, delay, timeout, len(content), content))
			print datas[0]
		except Exception, e:
			print e
	
	def peek(self,datas,type):
		try:
			datas = self.cliSend("peek-"+type)
			if(datas[1]):
				rts = datas[0].split(" ")
				print rts[1],":", datas[1]
		except Exception, e:
			print e

	def pauseTube(self,datas):
		try:
			timeout = 10
			if len(datas) > 1:
				timeout = int(datas[1])
			datas = self.cliSend("pause-tube %s %d"%(self.tube, timeout))
			print "Pause Tube %s %ds"%(self.tube, timeout)
		except Exception, e:
			print e

	def kickTube(self,datas):
		try:
			kickNum = 1
			if len(datas) > 1 and datas[1] != "":
				kickNum = int(datas[1])
			datas = self.cliSend("kick %d"%kickNum)
			print "Kick %d jobs To Ready Status "%(kickNum)
		except Exception, e:
			print e

	def use(self,datas):
		try:
			if len(datas) < 2 or datas[1] == "":
				raise Exception("[error]:Tube is Null.")
			tube = datas[1]
			datas = self.cliSend("use "+tube)
			print "change tube:"+tube
			self.tube = tube
		except Exception, e:
			print e

	# current stats
	def stats(self):
		try:
			datas = self.cliSend("stats")
			print datas
		except Exception, e:
			print e

	#list all exsit tubes
	def listTubes(self):
		tubes = []
		try:
			datas = self.cliSend("list-tubes")
			tubes = []
			for str in datas:
				if str[:2] == '- ':
					tubes.append(str[2:])
			i = 1
			for tube in tubes:
				print "%d) %s"%(i,tube)
				i = i+1
		except Exception, e:
			print e
		
	#Tube Stats
	def statsTube(self):
		try:				
			datas      = self.cliSend("stats-tube "+self.tube)
			tube_stats = {}
			for str in datas:
				lst = str.split(': ')
				if(len(lst) == 2):
					tube_stats[lst[0]] = lst[1]

			if tube_stats.get('name',None) != None:
				print 'Name:',tube_stats['name']
				print "Pause-Status:",tube_stats['pause']
				if tube_stats['pause'] > 0:
					print "Pause-Time-Left:",tube_stats['pause-time-left']					
				print "current-jobs-ready:",tube_stats['current-jobs-ready']
				print "current-jobs-reserved:",tube_stats['current-jobs-reserved']
				print "current-jobs-buried:",tube_stats['current-jobs-buried']
				print "current-jobs-delayed:",tube_stats['current-jobs-delayed']
				print "total-jobs:",tube_stats['total-jobs']
				print "current-watching:",tube_stats['current-watching']
				print "current-watching:",tube_stats['current-watching']

		except Exception, e:
			print e

	def __init__(self, host, port, tube, timeout=2.0):
		self.host    = host
		self.port    = port
		self.timeout = timeout
		self.tube    = tube
		self.cli = BeanstalkCli()
		self.cli.connect(self)

	def __del__(self):
		if self.socket != None:
			self.socket.close()

	def cliSend(self, command):
		result = self.cli.sendcommand(self, command)		
		datas  = result.split('\n')
		if len(datas) > 0 :
			command_excute_rs = datas[0]
			if command_excute_rs[:2] == 'OK':
				return datas[2:]
			elif command_excute_rs[:8] == 'WATCHING' or command_excute_rs[:5] == 'USING' or command_excute_rs[:5] == 'FOUND' or command_excute_rs[:6] == 'PAUSED' or command_excute_rs[:8] == 'INSERTED':
				return datas
			else:
				raise Exception(command_excute_rs)
		else:
			raise RuntimeError()
		exit()

#base socket operate
class BeanstalkCli:
	def connect(self,bts):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(bts.timeout)
		try:
			s.connect((bts.host, bts.port))
		except socket.timeout:
			print "connect socket timeout:%.2f s"%(bts.timeout)
		except Exception, e:
			print e
		else:
			bts.socket = s
			bts.socket.settimeout(None)

	def sendcommand(self, bts, command):
		command = command+"\r\n"
		datalen = 4096
		data    = ""
		bts.socket.sendall(command)
		while True:
			data = bts.socket.recv(datalen)
			if len(data) < datalen:
				break
		return data


if __name__ == '__main__':
	print "Cann't direct access module.\nMore Information You Can Communication With  Lailaiji@163.com"
	exit(1)