#
# connection.py
#

#
# connection.py
# Connection (C) 2014 Quytelda Gaiwin
#

import socket

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

import irc.connection

class Connection(LineReceiver):
	host = {'ip' : None, 'hostname' : None}
	server = None
	container = None

	def __init__(self, server):
		self.server = server
		self.container = irc.connection.IRCConnection(server, self)

	# this hook is called when a peer has initiated a connection
	# first we need to resolve the connection details
	def connectionMade(self):
		print '* connection established'
		
		# determine the peer's address and hostname
		self.message('NOTICE AUTH :*** Connection established; finding your hostname...')
		self.host['ip'] = self.transport.getPeer().host
		try:
			self.host['hostname'] = socket.gethostbyaddr(self.host['ip'])[0]
			self.message('NOTICE AUTH :*** Found your hostname (%s).' % self.host['hostname'])
		except socket.herror:
			self.message('NOTICE AUTH :*** Unable to resolve host; using peer IP.')

	def connectionLost(self, reason):
		print "* connection lost"
		
	def lineReceived(self, data):
		# if we are unregistered (we don't have a client or server container)
		# then we must send our requests directly to the server, and hope for approval
		self.container.handle_data(data)
		
	def message(self, msg, prefix = None):
		self.transport.write(":%s %s\r\n" % (prefix if (prefix != None) else self.server.name, msg))
		
	def numeric(self, numeric, nick, msg, prefix = None):
		if nick != None:
			self.message("%03d %s %s" % (numeric, nick, msg), prefix)
		else:
			self.message("%03d %s" % (numeric, msg), prefix)

class ConnectionFactory(protocol.Factory):
	
	def __init__(self, server):
		self.server = server

	def buildProtocol(self, addr):
		return Connection(self.server)
