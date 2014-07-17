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
	"""Server represents a running IRC server that accepts connections from clients and processes and executes commands from those clients.  It keeps track of (a) it's list of registered clients, (b) its list of existing channels, (c) its list of linked servers, and (d) all the metadata needed to run the service.  The server waits for incoming connections on the given port, and then passes them on to connection handlers (IRCConnection objects) when an external machine connects."""
	
	# server globals
	name = None # server name (doesn't need to match hostname)
	version = 'GreenIRCDv0.1u' # version string
	ports_client = [6667] # ports to list on (clients)
	ports_client_ssl = [6668] # port to listen on with SSL (clients)
	info = version
	admin_email = None
	config = None
	bans = []
	
	clients = {} # list of clients by nick
	servers = {} # list of servers by name
	hooks = {}	# list of command hooks by command
	channels = {} # list of channels by name (including prefixes)
	
	opers = [] # list of oper entries
	autojoin = '#green' # channel(s) to autojoin on connect
	operjoin = '#opers' # channel(s) to autojoin on oper
	
	connect_modes = 'ix'
	
	# we need a name to initialize the server
	def __init__(self, name):
		self.name = name
		self.register_hooks()

	def start(self):
		"""Attempts to start the server and listen for connections."""		
		for port in self.ports_client:
			reactor.listenTCP(port, connection.ConnectionFactory(self))
			print "* Listening on", port
		
		# listen for SSL connections on the given ports
		context = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')
		for port in self.ports_client_ssl:
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
			
			self.hooks[mod.__command__] = mod.handle_event
			
	def register_client(self, client, welcome = True):
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
			if (not source in self.clients.values()) and (not 'preregister' in dir(sys.modules[hook.__module__])):
				source.ctcn.numeric(symbols.ERR_NOTREGISTERED, None, ":You are not registered.")

			hook(self, source, msg.params)
