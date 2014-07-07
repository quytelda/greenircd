#
# connection.py
# Connection (C) 2014 Quytelda Gaiwin
#

# TODO: finish host cloaking
# TODO: vhosts
import hashlib

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

import symbols

class IRCConnection(LineReceiver):
	cloaked = True
	
	def __init__(self, server):
		self.server = server
		self.mode_stack = 0
	
	# this hook is called when a peer has initiated a connection
	# we must register the connection and wait for it to identify itself
	# TODO: hostname resolution	
	def connectionMade(self):
		peer_address = self.transport.getPeer().host
		#print self.transport.getPeer().getDestination().getHandle().getpeername()
		self.server.send_msg(self, 'NOTICE AUTH :*** Connection established!')
	
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
	
	# returns the host string for this user as it should be seen by other users
	# applies vhosts and cloaks
	def host(self, cloak = True):
		host = self.vhost if hasattr(self, 'vhost') else self.transport.getPeer().host
		if self.has_mode('x') and cloak: host = hashlib.sha256(host).hexdigest()[0:len(host)]
		return host
	
	# convenience method to test if a user has a mode flag
	def has_mode(self, flag):
		return (self.mode_stack & symbols.user_modes[flag]) > 0

class IRCConnectionFactory(protocol.Factory):

	def __init__(self, server):
		self.server = server

	def buildProtocol(self, addr):
		return IRCConnection(self.server)
