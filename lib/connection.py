import socket

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

class Connection(LineReceiver):

	def __init__(self, factory):
		self.factory = factory
		self._id = None


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

		self.factory.server.handle_message(self._id, data)


	def message(self, msg, prefix = None):
		"""
		Sends a message to the client socket, appropriately prefixed and
		padded with the requisite CR-LF delimiter.
		"""
		self.transport.write(":%s %s\r\n" % \
							 (prefix if (prefix is not None) else self.factory.server.name, msg))


class ConnectionFactory(protocol.Factory):

	def __init__(self, server):
		self.server = server


	def buildProtocol(self, addr):
		return Connection(self)
