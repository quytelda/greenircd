import socket

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

class Connection(LineReceiver):

	def __init__(self, factory):
		self.factory = factory
		self.name = None


	def connectionMade(self):

		# resolve peer connection details
		self.host = self.transport.getPeer().host

		try:
			self.host = socket.gethostbyaddr(self.host)[0]
		except socket.herror:
			print("* Unable to resolve hostname.")

		print("Connection established from %s." % self.host)


	def connectionLost(self, reason):

		print("Connection lost from %s." % self.host)


	def lineReceived(self, data):

		self.factory.server.handle_message(self, self.name, data)


	def message(self, prefix, message):

		self.transport.write(":%s %s\r\n" % (prefix, message))


	def numeric(self, prefix, numeric, nick, message):
		self.message(prefix, "%03d %s %s" % (numeric, nick, message))


class ConnectionFactory(protocol.Factory):

	def __init__(self, server):
		self.server = server


	def buildProtocol(self, addr):
		return Connection(self)
