from lib import numeric
from lib.module import Module

from lib.error import NameInUseError

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
			self.server.change_nick(source, nick)
		except NameInUseError as err:
			err.ctcn.numeric(self.server.name, numeric.ERR_NICKNAMEINUSE, nick, ":Nickname already in use.")
		except NoSuchTargetError as err:
			err.ctcn.numeric(self.server.name, numeric.ERR_NOSUCHNICK, nick, ":No such nickname.")
