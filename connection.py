#
# connection.py
# Connection (C) 2014 Quytelda Gaiwin
#

# TODO: finish host cloaking
# TODO: vhosts
import hashlib
import socket

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

import symbols

class IRCConnection(LineReceiver):
	rhost = None
	vhost = None
	
	def __init__(self, server):
		self.server = server
		self.mode_stack = 0
	
	# this hook is called when a peer has initiated a connection
	# we must register the connection and wait for it to identify itself
	# TODO: hostname resolution	
	def connectionMade(self):
		peer_address = self.transport.getPeer().host
		self.server.send_msg(self, 'NOTICE AUTH :*** Connection established; finding your hostname...')
		try:
			host = socket.gethostbyaddr(peer_address)
			self.server.send_msg(self, 'NOTICE AUTH :*** Found your hostname (%s).' % host[0])
			self.rhost = host[0]
		except socket.herror:
			self.rhost = peer_address
			self.server.send_msg(self, 'NOTICE AUTH :*** Unable to resolve host; using peer IP.')

	def connectionLost(self, reason):
		print "* connection lost!"
		self.server.unregister_connection(self)
		
	def lineReceived(self, data):
		self.server.handle_message(self, data)
		
	def close(self):
		self.transport.loseConnection()

	def get_hostmask(self):
		# hostmasks for clients are in the form:
		# <nick>!<username>@<host>
		if hasattr(self, 'nick') and hasattr(self, 'uid'):
			host = self.host()
			return "%s!%s@%s" % (self.nick, self.uid, host)
	
	# returns the host string for this user
	# applies vhosts and cloaks as needed
	def host(self, cloak = True, vhost = True):
		if (self.vhost != None) and vhost and self.has_mode('t'):
			return self.vhost
		elif cloak and self.has_mode('x'):
			return 'cloaked-address'
		else:
			return self.rhost

	# convenience method to test if a user has a mode flag
	def has_mode(self, flag):
		return (self.mode_stack & symbols.user_modes[flag]) > 0

class IRCConnectionFactory(protocol.Factory):

	def __init__(self, server):
		self.server = server

	def buildProtocol(self, addr):
		return IRCConnection(self.server)
