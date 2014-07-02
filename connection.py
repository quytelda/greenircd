#
# connection.py
# Connection (C) 2014 Quytelda Gaiwin
#
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

import symbols

class IRCConnection(LineReceiver):
	def __init__(self, server):
		self.server = server
		self.mode_stack = 0
	
	# this hook is called when a peer has initiated a connection
	# we must register the connection and wait for it to identify itself
	# TODO: hostname resolution	
	def connectionMade(self):
		peer_address = self.transport.getPeer().host
		self.server.send_msg(self, 'NOTICE AUTH :*** Connection established!')
	
	def connectionLost(self, reason):
		print "* connection lost!"
		self.server.unregister_connection(self)
		
	def lineReceived(self, data):
		self.server.handle_message(self, data)
		
	def kill(self):
		self.transport.loseConnection()

	def get_hostmask(self):
		if hasattr(self, 'nick') and hasattr(self, 'uid'):
			return "%s!%s@%s" % (self.nick, self.uid, self.transport.getPeer().host)
		else:
			return "server.host"
	
	# convenience method to test if a user has a mode flag
	def has_mode(self, flag):
		return (self.mode_stack & symbols.user_modes[flag]) > 0

class IRCConnectionFactory(protocol.Factory):

	def __init__(self, server):
		self.server = server

	def buildProtocol(self, addr):
		return IRCConnection(self.server)
