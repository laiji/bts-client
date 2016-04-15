#!/usr/bin/python
from libs.beanstalkd import Beanstalk
import sys

commands = {
	"listTubes":lambda bts,datas:bts.listTubes(),
	"statsTube":lambda bts,datas:bts.statsTube(),
	"stats":lambda bts,datas:bts.stats(),
	"use":lambda bts,datas:bts.use(datas),
	"put":lambda bts,datas:bts.put(datas),
	"pause":lambda bts,datas:bts.pauseTube(datas),
	"kick":lambda bts,datas:bts.kickTube(datas),
	"peekReady":lambda bts,datas:bts.peek(datas,'ready'),
	"peekDelayed":lambda bts,datas:bts.peek(datas,'delayed'),
	"peekBuried":lambda bts,datas:bts.peek(datas,'buried'),
}

if __name__ == '__main__':
	argvs = sys.argv[1:]
	if len(argvs) < 1:
		print "Using: bts-cli 127.0.0.1 11300"
		exit(1)
	for str in argvs:
		if str == '-h' or str == '--help':
			print "Using: bts-cli 127.0.0.1 11300"
			exit(1);
	_host = argvs[0];
	_port = int(argvs[1]);
	_tube = 'default'
	bts   = Beanstalk(_host,_port,_tube)
	while True:
		try:			
			buf        = raw_input("%s:%d[%s]>"%(_host, _port, _tube))
			bufs       = buf.split(' ');
			subCommand = bufs[0];
			if commands.get(subCommand, None) != None:
				commands[subCommand](bts,bufs)
				if subCommand == 'use':
					_tube = bufs[1]
			elif subCommand == 'quit':
				exit(0)
			elif subCommand == 'help':
				for cmd in commands.keys():
					print cmd
			else:
				print "UnSupport this command:",buf
		except KeyboardInterrupt,e:
			print "\nBye Bye~"
			exit();
		except Exception, e:
			print e
		