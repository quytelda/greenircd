from lib import numeric
from lib.module import Module

from lib.error import NameInUseError

class NickMod(Module):

	command = "PRIVMSG"

	def handle_unreg(self, source, message):
		source.numeric(self.server.name, numeric.ERR_NOTREGISTERED, nick, ":Not registered.")

	def handle_client(self, source, message):

		if len(message['params']) < 1:
			return

		target = message['params'][0]
		msg = message['params'][1]

		self.server.message_client(target, source, "PRIVMSG %s :%s" % (target, msg))
