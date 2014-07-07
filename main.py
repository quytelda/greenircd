#!/usr/bin/python
# main.py
#
# Copyright (C) 2014 Quytelda Gaiwin

import os
import re
import ConfigParser
from server import IRCServer, OperEntry

def main(path):

	server = IRCServer()
#	server.start()

	parser = ConfigParser.ConfigParser()
	parser.read(path)
	
	# try to parse values
	for section in parser.sections():
		if section.startswith('server:'):
			setattr(server, 'name', section.replace('server:', ''))
			for directive in parser.options(section):
				value = parser.get(section, directive)
				server.set_attribute(directive, value)
		if section.startswith('oper:'):
			options = parser.options(section)
			
			# parse out the username
			uname = section.replace('oper:', '')
			
			# get the authentication hash
			if not 'auth' in options:
				print 'Oper entry missing "auth" directive for', uname
				continue
			auth = parser.get(section, 'auth')
			
			# create an OperEntry object
			oper = OperEntry(uname, auth)
			
			if 'flags' in options:
				setattr(oper, 'flags', parser.get(section, 'flags'))
				
			server.opers.append(oper)

	server.start()

def set_attribute(srv, key, value):
	if key == 'port':
		setattr(srv, key, int(value))
	#elif key == 'auto-join':
	#	srv.autojoin.append[value]
	else:
		print "Config Error: Unrecognized directive: %s"

main('greenircd.conf')
