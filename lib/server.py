import importlib

import mod
import lib.module
from lib import numeric
from lib.channel import Channel

from lib.error import NoSuchTargetError, NameInUseError

MODULE_PKG = 'mod'
mods = ['nick', 'quit']

class Server(object):

	def __init__(self, name):
		self.name = name
		self.clients = {}
		self.servers = {}

		self.channels = {}

		self.__command_handlers = {}

		for mod in mods:
			self.__load_module(mod)


	def message_client(self, nick, prefix, message):

		if nick not in self.clients:
			raise NoSuchTargetError

		client = self.clients[nick]
		client.message(prefix, message)


	def message_channel(self, target, command, prefix = None, params = None):

		# TODO: check if channel exists
		channel = self.channels[target]

		for nick in channel.members:
			self.message_client(nick, prefix, command, params)


	def message_common(self, nick, prefix, command, params):

		#TODO: check if nickname exists
		for target in self.channels:
			if nick in channels[target]:
				self.message_channel(target, prefix, command, params)


	def disconnect_client(self, nick):

		#TODO: check if nick exists

		client = self.clients[nick]
		client.transport.loseConnection()

		# remove the user from the registration
		del self.clients[nick]


	def register_client(self, nick, connection):

		# nicknames must be unique
		if nick in self.clients:
			connection.numeric(self.name, numeric.ERR_NICKNAMEINUSE, nick, ":Nickname already in use")
			return

		# add to client dict
		self.clients[nick] = connection
		connection.name = nick

		# send welcome
		connection.numeric(self.name, numeric.RPL_WELCOME, nick, ":Welcome to GreenIRCD")

	def __format_message(self, prefix, command, params):
		message = ":%s %s %s " % \
				  (prefix, command, ' '.join(params[ : -1]))

		if ' ' in params[-1]:
			message += ":"
		message += params[-1]

		return message


	def handle_message(self, ctcn, id, message):

		command = _parse_message(message)

		# ignore unknown commands
		if command['command'] not in self.__command_handlers:
			print("Received unknown command: %s" % command['command'])
			return

		handler = self.__command_handlers[command['command']]
		if id in self.clients:
			print("%s (client): %s" % (id, command))
			handler.handle_client(id, command)
		elif id in self.servers:
			print("%s (server): %s" % (id, command))
			handler.handle_server(id, command)
		else:
			print("%s (unreg): %s" % (id, command))
			handler.handle_unreg(ctcn, command)



	def __load_module(self, name):

		try:
			import inspect

			module = importlib.import_module('.' + name, MODULE_PKG)
			mod_classes = [x[1] \
						   for x in inspect.getmembers(module, inspect.isclass) \
						   if (issubclass(x[1], lib.module.Module)) and (x[0] != 'Module')]

			for cls in mod_classes:
				obj = cls(self)
				self.__command_handlers[obj.command] = obj

			print("* Loaded module: %s" % name)

		except ImportError:
			print("* Failed to load module: %s" % name)


def _parse_message(raw):

	message = {}
	elems = raw.strip().split(' ')

	if len(raw) == 0:
		return None

	# prefix
	if elems[0].startswith(':'):
		message['prefix'] = elems.pop(0)
	else:
		message['prefix'] = None

	# command
	message['command'] = elems.pop(0).upper()

	# parameters
	message['params'] = []

	for i in range(0, len(elems)):
		if elems[i].startswith(':'):
			message['params'].append(' '.join(elems[i:]))
			break

		message['params'].append(elems[i])

	return message
