from lib import numeric
from lib.module import Module

from lib.error import NameInUseError, NoSuchTargetError

class NickMod(Module):

	command = "NICK"

	def handle_unreg(self, source, message):

		# TODO: verbose error
		if len(message['params']) < 1:
			return
		nick = message['params'][0]

		try:
			self.server.register_client(nick, source)
		except NameInUseError as err:
			err.ctcn.numeric(self.server.name, numeric.ERR_NICKNAMEINUSE, nick, ":Nickname already in use.")

	def handle_client(self, source, message):

		if len(message['params']) < 1:
			return

		nick = message['params'][0]

		try:
			# ignore changes to same nick
			if source == nick: return

			# apply
			self.server.change_nick(source, nick)
			self.server.message_client(nick, source, "NICK %s" % nick)

		except NameInUseError as err:
			self.server.numeric_message_client(self.server.name, numeric.ERR_NICKNAMEINUSE, source, ":Nickname already in use.")
		except NoSuchTargetError as err:
			self.server.numeric_message_client(self.server.name, numeric.ERR_NOSUCHNICK, source, ":No such nickname.")
