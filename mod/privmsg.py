from lib import numeric
from lib.module import Module

from lib.error import NameInUseError

from lib.error import NoSuchTargetError

class NickMod(Module):

	command = "PRIVMSG"

	def handle_unreg(self, source, message):
		source.numeric(self.server.name, numeric.ERR_NOTREGISTERED, "*", ":Not registered.")

	def handle_client(self, source, message):

		if len(message['params']) < 1:
			return

		target = message['params'][0]
		msg = message['params'][1]

		try:
			self.server.message_client(target, source, "PRIVMSG %s :%s" % (target, msg))
		except NoSuchTargetError as err:
			self.server.numeric_message_client(self.server.name, numeric.ERR_NOSUCHNICK, source, ":No such nickname.")
