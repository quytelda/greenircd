from lib import numeric
from lib.module import Module

from lib.error import NameInUseError, NoSuchTargetError

class PingMod(Module):

	command = "PING"

	def handle_client(self, source, message):

		response = self.server.name
		if len(message['params']) > 0:
			response = message['params'][0]

		self.server.message_client(source, self.server.name, "PONG :%s" % response)
