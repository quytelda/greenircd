from lib.module import Module

class NickMod(Module):

	command = "NICK"

	def handle_unreg(self, source, message):

		# TODO: verbose error
		if len(message['params']) < 1:
			return

		nick = message['params'][0]
		self.server.register_client(nick, source)
