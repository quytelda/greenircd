#
# server.py
# Copyright (C) 2014 Quytelda Gaiwin
#

import sys

from twisted.internet import ssl, reactor, endpoints

from irc.connection import IRCConnection
from irc.client import IRCClient
from irc.server import IRCServer
from irc.message import IRCMessage

import connection
import channel
import symbols
import modules
from modules import *

class Server:
	"""
	Server represents a running instance of the local IRC server,
	which accepts connections from clients and processes and executes messages from those clients.
	Server maintains a representation of the networks state, which should theoretically match on each server.
	This includes a list of clients, channels, modes, and bans.

	The server waits for incoming connections on the given port,
	and then passes them on to connection handlers (IRCConnection objects) when an external machine connects.
	"""

	# server globals
	name = None # server name (need not match the actual hostname)
	version = 'GreenIRCDv0.1u' # version string
	ports_client = [6667] # ports to list on (clients)
	ports_client_ssl = [6668] # port to listen on with SSL (clients)
	ports_server = [] # ports to list on (servers)
	ports_server_ssl = [] # port to listen on with SSL (servers)
	hooks = {}	# list of command hooks by command
	
	opers = [] # list of oper entries
	links = {} # list of link entries
	bans = [] # list of banned hosts
	autojoin = '#green' # channel(s) to autojoin on connect
	operjoin = '#opers' # channel(s) to autojoin on oper
	info = version
	config = None
	
	# administrative information fields
	admin_lines = []
	admin_email = None
	
	# network structures
	clients = {} # list of clients by nick
	servers = {} # list of servers by name
	channels = {} # list of channels by name (including prefixes)
	
	connect_modes = 'ix' # modes to assign upon registration
	
	# we need a name to initialize the server
	def __init__(self, name):
		self.name = name
		self.register_hooks()

	def start(self):
		"""Attempts to start the server and listen for connections on whatever ports are designated."""	
		# listen for TCP connections on the given ports	
		for port in self.ports_client + self.ports_server:
			reactor.listenTCP(port, connection.ConnectionFactory(self))
			print "* Listening on", port
		
		# listen for SSL connections on the given ports
		context = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')
		for port in self.ports_client_ssl + self.ports_server_ssl:
			reactor.listenSSL(port, connection.ConnectionFactory(self, ssl = True), context)
			print "* Listening on", port, "(SSL)"
		
		# run the reactor (start accepting connections)
		reactor.run()
		
	def register_hooks(self):
		"""Finds and registers all command hooks from the correct package."""
		for module in dir(modules):
			if module.startswith('__'): continue

			print "* loading module:", module

			# add the module's hook to the dictionary
			mod = sys.modules['modules.%s' % module]

			if not hasattr(mod, '__command__'):
				print "** FAIL: unable to load '%s' because __command__ is not set." % module
				continue

			self.hooks[mod.__command__] = mod.handle_event

	def register_client(self, client, welcome = True):
		"""
		When a client connects to the IRC network, it must be registered with the server to send and receive messages on the network.
		This method adds the client to the server's registration list.
		"""
		if not isinstance(client, IRCClient) or (client.nick == None):
			return

		self.clients[client.nick] = client
		if welcome:
			self.welcome_client(client)
			sendsno.handle_event(self, None, ['s', "Notice: New client has registered on this server (%s)." % client.hostmask()])

	def unregister_client(self, client):
		"""Attempts to reverse the effects of registering a client with the server."""
		if not isinstance(client, IRCClient) or (client.nick == None) or (not client.nick in self.clients):
			return

		del self.clients[client.nick]
		print "* Client (%s) unregistered" % client.hostmask()

	def update_client(self, client, old_nick):
		if not isinstance(client, IRCClient) or (client.nick == None):
			return

		if (old_nick != None) and (old_nick in self.clients):
			del self.clients[old_nick]

		self.register_client(client, welcome = (old_nick == None))

	def welcome_client(self, client):
		# send the welcome information
		client.ctcn.numeric(symbols.RPL_WELCOME, client.nick, "Welcome to %s, %s!" % (self.name, client.nick))
		modules.version.handle_event(self, client, [])

		# set welcome modes
		mode_string = '+' + self.connect_modes
		if client.ctcn.ssl: mode_string += 'z'
		print client.ctcn.ssl
		modules.mode.handle_event(self, client, [client.nick, mode_string])


		# autojoin channels in the autojoin list
		if len(self.autojoin) > 0:
			modules.join.handle_event(self, client, [self.autojoin])
			
	def register_server(self, server):
		self.servers[server.name]

	def unregister_server(self, server):
		del self.servers[server.name]

	def announce(self, msg, prefix, exclude = None):
		"""Sends a message to every client registered with the server"""
		for client in self.clients.values():
			if client == exclude: continue
			client.ctcn.message(msg, prefix)

	def announce_channel(self, channel, msg, prefix, exclude = None):
		"""Sends a message to every client in the channel"""
		for client in channel.members:
			if client == exclude: continue
			client.ctcn.message(msg, prefix)

	def announce_common(self, client, msg, prefix, exclude = None):
		"""Sends a message to all clients in a common channel with the given client."""
		for channel in self.channels.values():
			if client in channel.members:
				self.announce_channel(channel, msg, prefix, exclude)

	# TODO command vs numeric vs garbage
	def handle_message(self, source, data):
		"""Handles and incoming message from a connection.  Usually, this will just pass it on to the command handler."""
		message = data.strip()

		# attempt to parse the message
		msg = IRCMessage(message)
		self.do_command(source, msg)

	def do_command(self, source, msg):
		"""Attempts to execute a command with the corresponding command handle (loaded as a module with a handle_event method)."""
		# attempt to handle the command with the correct hook module
		if msg.command.upper() in self.hooks:
			hook = self.hooks[msg.command.upper()]
			if (not source in (self.clients.values() + self.servers.values())) and (not 'preregister' in dir(sys.modules[hook.__module__])):
				print source, '! in', self.clients.values()
				source.ctcn.numeric(symbols.ERR_NOTREGISTERED, None, ":You are not registered.")

			hook(self, source, msg.params)
