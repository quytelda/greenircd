import lib.module as module
from lib import numeric

from lib.error import NameInUseError, NoSuchTargetError

class KillMod(module.Module):

	command = "KILL"

	@module.min_params(1)
	def handle_client(self, source, message):
		nick = message['params'][0]

		try:

			# generate QUIT event
			message = {
				'prefix' : None,
				'command' : 'QUIT',
				'params' : ['Disconnected by %s.' % source]
			}

			self.server.generate_client_event(nick, message)

		except NameInUseError as err:
			self.server.numeric_message_client(self.server.name,
											   numeric.ERR_NICKNAMEINUSE,
											   source,
											   ":Nickname already in use.")
		except NoSuchTargetError as err:
			self.server.numeric_message_client(self.server.name,
											   numeric.ERR_NOSUCHNICK,
											   source,
											   ":No such nickname.")
