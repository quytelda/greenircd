import importlib

import mod
import lib.module
from lib import numeric
from lib.channel import Channel

from lib.error import NoSuchTargetError, NameInUseError

MODULE_PKG = 'mod'
mods = ['nick', 'quit', 'privmsg', 'kill']

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
		"""
		Send a message to the client with this nickname.
		"""

		if nick not in self.clients:
			raise NoSuchTargetError(nick)

		client = self.clients[nick]
		client.message(prefix, message)


	def numeric_message_client(self, prefix, numeric, nick, message):
		"""
		Send a numeric message to the client with this nickname.
		"""
		self.message_client(nick, prefix, "%03d %s %s" % (numeric, nick, message))


	def message_channel(self, target, command, prefix = None, params = None):
		"""
		Send a message to every client in the channel `target`.
		"""

		# TODO: check if channel exists
		channel = self.channels[target]

		for nick in channel.members:
			self.message_client(nick, prefix, command, params)


	def message_common(self, nick, prefix, command, params):
		"""
		Send a message to every client that has joined at least
		one channel in common with `nick`.

		BUG: joining > 1 common channel results in duplicate messages
		TODO: filter duplicates
		"""

		if nick not in self.clients:
			raise NoSuchTargetError(nick)

		for target in self.channels:
			if nick in channels[target]:
				self.message_channel(target, prefix, command, params)


	def disconnect_client(self, nick):
		"""
		Remove a client from the server's client list, then terminate the connection.
		"""

		if nick not in self.clients:
			raise NoSuchTargetError(nick)

		client = self.clients[nick]
		client.transport.loseConnection()

		# remove the user from the registration
		del self.clients[nick]


	def register_client(self, nick, connection):
		"""
		Add a client to the server's registered client list,
		then send welcome information.
		"""

		# nicknames must be unique
		if nick in self.clients:
			raise NameInUseError(nick, connection)

		# add to client dict
		self.clients[nick] = connection
		connection.name = nick

		# send welcome
		self.numeric_message_client(self.name, numeric.RPL_WELCOME, nick, ":Welcome to GreenIRCD")


	def change_nick(self, old_nick, new_nick):
		"""
		Attempt to change a client's unique nickname.
		"""

		if old_nick not in self.clients:
			raise NoSuchTargetError(old_nick)

		if new_nick in self.clients:
			raise NameInUseError(new_nick)

		# swap
		ctcn = self.clients[old_nick]
		del self.clients[old_nick]
		self.clients[new_nick] = ctcn

		ctcn.name = new_nick


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


	def generate_client_event(self, target, message):
		"""
		Generate and execute an event as if it had been issued
		by the client with the given nickname.
		"""

		if target not in self.clients:
			raise NoSuchTargetError(target)

		handler = self.__command_handlers[message['command']]
		handler.handle_client(target, message)


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
			message['params'].append(' '.join(elems[i:])[1:])
			break

		message['params'].append(elems[i])

	return message
