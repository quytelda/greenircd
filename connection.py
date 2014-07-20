#
# connection.py
#

#
# connection.py
# Connection (C) 2014 Quytelda Gaiwin
#

import socket

from twisted.internet import protocol, task
from twisted.protocols.basic import LineReceiver

import irc.connection

import modules.quit

class Connection(LineReceiver):
	def __init__(self, server, ssl = False):
		self.host = {'ip' : None, 'hostname' : None}
		self.ssl = ssl
		self.server = server
		self.container = irc.connection.IRCConnection(server, self)
		self.alive = True

		self.alive_timer = task.LoopingCall(self.check_alive)
		self.alive_timer.start(30)

	# this hook is called when a peer has initiated a connection
	# first we need to resolve the connection details
	def connectionMade(self):
		"""
		This hooks is triggered when a peer has initiated a connection to the server.
		Here the connection details (peer IP and hostname) are resolved.
		"""
		print '* connection established on port %s (%s)' % (self.transport.getHost().port, self.container.host(False))
		
		# determine the peer's address and hostname
		self.message('NOTICE AUTH :*** Connection established; finding your hostname...')
		self.host['ip'] = self.transport.getPeer().host
		try:
			self.host['hostname'] = socket.gethostbyaddr(self.host['ip'])[0]
			self.message('NOTICE AUTH :*** Found your hostname (%s).' % self.host['hostname'])
		except socket.herror:
			self.message('NOTICE AUTH :*** Unable to resolve host; using peer IP.')

	def connectionLost(self, reason):
		print "* connection lost (%s)" % self.host
		
	def lineReceived(self, data):
		"""
		Receives lines of data (separated by CR-LF) from the client, and passes them to the central server for processing
		via the connection's container object (which is or needs to be registered with the server).
		"""
		self.container.handle_data(data)
		
	def check_alive(self):
		"""
		This method, called at regular intervals, checks to see if the client has sent any data (probably a PONG message)
		since the last PING message from the server.If not, the connection is considered dead and is terminated;
		otherwise, another PING message is sent.
		"""
		# if the last ping wasn't reciprocated, kill the connection
		# (generate a QUIT event with the appropriate reason)
		if not self.alive:
			modules.quit.handle_event(self.server, self.container, ['Ping Timeout'])
			return

		# ping the client anew
		# for some reason, the PING message should *not* be prefixed
		if isinstance(self.container, irc.client.IRCClient):
			self.transport.write("PING :%s\r\n" % self.server.name)

		self.alive = False

	def message(self, msg, prefix = None):
		"""Sends a message to the client socket, appropriately prefixed and padded with the requisite CR-LF delimiter."""
		self.transport.write(":%s %s\r\n" % (prefix if (prefix != None) else self.server.name, msg))
		
	def numeric(self, numeric, nick, msg, prefix = None):
		"""
		Sends a properly formatted numeric message to the client.
		The message receives the proper prefix and CR-LF via connection.message().
		"""
		if nick != None:
			self.message("%03d %s %s" % (numeric, nick, msg), prefix)
		else:
			self.message("%03d %s" % (numeric, msg), prefix)

class ConnectionFactory(protocol.Factory):
	
	def __init__(self, server, ssl = False):
		self.server = server
		self.ssl = ssl

	def buildProtocol(self, addr):
		return Connection(self.server, self.ssl)
