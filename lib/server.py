import importlib

import lib.module
from lib.channel import Channel
import mod

MODULE_PKG = 'mod'
mods = ['nick']

class Server(object):

	def __init__(self, name):
		self.name = name
		self.clients = {}
		self.servers = {}

		self.channels = {}

		self.__command_handlers = {
			'client' : {},
			'server' : {},
			'unreg' : {}
		}

		for mod in mods:
			self.__load_module(mod)

		print(self.__command_handlers)


	def message_client(self, nick, prefix, command, params):

		# TODO: check if nick isn't in the dict
		message = self.__format_message(prefix, command, params)
		print(message)


	def message_channel(self, target, prefix, command, params):

		# TODO: check if channel exists
		channel = self.channels[target]

		for nick in channel.members:
			self.message_client(nick, prefix, command, params)


	def message_common(self, nick, prefix, command, params):

		#TODO: check if nickname exists
		for target in self.channels:
			if nick in channels[target]:
				self.message_channel(target, prefix, command, params)


	def disconnect_client(self, nick, reason):

		#TODO: check if nick exists

		client = clients[nick]
		client.transport.loseConnection()

		# remove the user from the registration
		del clients[nick]


	def register_client(self, nick, connection):

		#TODO: ensure nick doesn't already exist
		clients[nick] = connection


	def __format_message(self, prefix, command, params):
		message = ":%s %s %s " % \
				  (prefix, command, ' '.join(params[ : -1]))

		if ' ' in params[-1]:
			message += ":"

		message += params[-1]

		return message

	def handle_message(self, id, message):

		command = _parse_message(message)

		type = None
		if id in self.clients:
			print("%s (client): %s" % (id, command))
			type = 'client'
		elif id in self.servers:
			print("%s (server): %s" % (id, command))
			type = 'server'
		else:
			print("%s (unreg): %s" % (id, command))
			type = 'unreg'

		self.__handle_command(command, type)

	def __handle_command(self, command, type):

		# TODO: check if handle exists
		handle = self.__command_handlers[type][command['command']]
		handle(command['prefix'], command['params'])


	def __load_module(self, name):

		try:
			import inspect

			module = importlib.import_module('.' + name, MODULE_PKG)
			mod_objects = [x[1] \
						   for x in inspect.getmembers(module, inspect.isclass) \
						   if issubclass(x[1], lib.module.Module)]

			# enumerate handlers
			isfunction = lambda x: inspect.isfunction(x) or inspect.ismethod(x)
			for obj in mod_objects:
				for function in inspect.getmembers(obj, isfunction):
					elems = function[0].split('_')

					# ignore invalid functions
					if (elems[0] != "handle") or \
					   (len(elems) != 3) or \
					   (elems[1] not in self.__command_handlers):
						continue

					type = elems[1]
					cmd = elems[2]
					self.__command_handlers[type][cmd] = function[1]

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
