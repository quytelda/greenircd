#
# irc/connection.py
#

import socket

class IRCConnection:
	ctcn = None
	server = None
	
	def __init__(self, server, ctcn):
		self.ctcn = ctcn
		self.server = server
		
		ctcn.container = self
	
	def handle_data(self, data):
		"""Passes the server the data from the connection.  In the future, this message should ensure that this is (a) allowed, and (b) valid."""
		self.server.handle_message(self, data)
		
	# TODO implement cloaking
	def host(self, cloak = True):
		return self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']
		
	def terminate(self):
		self.ctcn.transport.loseConnection()
