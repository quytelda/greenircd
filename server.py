#
# server.py
# Copyright (C) 2014 Quytelda Gaiwin
#

import sys

from twisted.internet import reactor, endpoints

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
	version = 'GreenIRCDv1.0u' # version string
	port = 6667 # port to list on
	info = "Tamalin (http://www.tamalin.org) GreenIRCd"
	
	clients = {} # list of clients by nick
	servers = {} # list of servers by name
	hooks = {}	# list of command hooks by command
	channels = {} # list of channels by name (including prefixes)
	
	opers = [{'username' : "quytelda", 'auth' : "d54479b4c6a321aabd090a5b9fcf3a5e3240ad643a6f349c2f59ed10f3b703a4", 'flags' : "owqa"}] # list of oper entries
	autojoin = '#green' # channel(s) to autojoin on connect
	operjoin = '#opers' # channel(s) to autojoin on oper
	
	# we need a name to initialize the server
	def __init__(self, name):
		self.name = name
		self.register_hooks()

	def start(self):
		"""Attempts to start the server and listen for connections."""		
		self.endpoint = endpoints.TCP4ServerEndpoint(reactor, self.port)
		self.endpoint.listen(connection.ConnectionFactory(self))
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

	def register_connection(self, ctcn):
		return
			
	def register_client(self, client, welcome = True):
		if not isinstance(client, IRCClient) or (client.nick == None):
			return

		self.clients[client.nick] = client
		if welcome: self.welcome_client(client)
		
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
		chan_modes = [symbols.status_modes[x]['modechar'] for x in sorted(symbols.status_modes, reverse=True)]
		chan_prefixes = [symbols.status_modes[x]['prefix'] for x in sorted(symbols.status_modes, reverse=True)]

		client.ctcn.numeric(symbols.RPL_WELCOME, client.nick, "Welcome to %s, %s!" % (self.name, client.nick))
		client.ctcn.numeric(symbols.RPL_YOURHOST, client.nick, ':Your host is %s, running version %s' % (self.name, self.version))
		client.ctcn.numeric(symbols.RPL_MYINFO, client.nick, '%s %s %s %s' % (self.name, self.version, ''.join(symbols.user_modes.keys()), ''.join(symbols.chan_modes.keys())))
		client.ctcn.numeric(symbols.RPL_ISUPPORT, client.nick, 'PREFIX=(%s)%s :are supported' % (''.join(chan_modes), ''.join(chan_prefixes)))

		# set welcome modes
		modules.mode.handle_event(self, client, [client.nick, '+ix'])

		# autojoin channels in the autojoin list
		if len(self.autojoin) > 0:
			modules.join.handle_event(self, client, [self.autojoin])
		
	def announce(self, msg, prefix, exclude = None):
		"""Sends a message to every client registered with the server"""
		for client in self.clients.values():
			if client == exclude: continue
			print "*** messaging", client.nick
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
