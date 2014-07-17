#
# irc/connection.py
#

import socket
import hashlib

class IRCConnection:	
	def __init__(self, server, ctcn):
		self.ctcn = ctcn
		self.server = server
		
		ctcn.container = self
	
	def handle_data(self, data):
		"""Passes the server the data from the connection.  In the future, this message should ensure that this is (a) allowed, and (b) valid."""
		# if data has been received, the connection is indeed alive
		# mark it alive, and reset the timer
		self.ctcn.alive = True
		self.ctcn.alive_timer.reset()

		self.server.handle_message(self, data)
		
	# TODO implement cloaking
	def host(self, cloak = True):
		rhost = self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']
		return rhost

	def terminate(self):
		self.ctcn.transport.loseConnection()
