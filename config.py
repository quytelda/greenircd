#
# config.py
#

import ConfigParser

def config(srv, path, init = True):
	parser = ConfigParser.ConfigParser()
	parser.read(path)
	
	srv.config = path
	srv.opers = []

	for section in parser.sections():
		if section.startswith('server:'):
			# get name
			if init:
				srv.name = section.replace('server:', '')
			
			# get port
			if ('port' in parser.options(section)) and init:
				srv.port = int(parser.get(section, 'port'))
				
			# get info
			if 'info' in parser.options(section):
				srv.info = parser.get(section, 'info')
				
			# autojoin
			if 'autojoin' in parser.options(section):
				srv.autojoin = parser.get(section, 'autojoin')
				
			if 'operjoin' in parser.options(section):
				srv.operjoin = parser.get(section, 'operjoin')
				
			if 'connect-modes' in parser.options(section):
				srv.connect_modes = parser.get(section, 'connect-modes')
				
		if section.startswith('oper:'):
			oper = {}
		
			# get login
			oper['username'] = section.replace('oper:', '')
			
			# get auth
			oper['auth'] = parser.get(section, 'auth')
			
			# get flags
			if 'flags' in parser.options(section):
				oper['flags'] = parser.get(section, 'flags')
			else:
				oper['flags'] = 'o'
				
			srv.opers.append(oper)
