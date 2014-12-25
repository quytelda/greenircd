from lib.module import Module

class QuitMod(Module):

	command = "QUIT"

	def handle_unreg(self, source, message):

		# nothing has been registered with the server yet
		# so we can just go ahead and kill the connection
		source.transport.loseConnection()

	def handle_client(self, source, message):

		reason = ""
		if len(message['params']) > 0:
			reason = message['params'][0]

		self.server.message_client(source, source, "QUIT %s" % reason)
		self.server.disconnect_client(source)
