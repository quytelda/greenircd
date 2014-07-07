#
# server.py
# Copyright (C) 2014 Quytelda Gaiwin
#

#!/usr/bin/python

import sys

from twisted.internet import reactor, endpoints

import connection
import channel
import symbols
import modules
from modules import *

class IRCServer:
	version = 'GreenIRCDv0.1'
	port = 6667
	opers = []
	autojoin = ''
	operjoin = ''

	def __init__(self):
		self.clients = {}
		self.servers = {}
		self.hooks = {}
		
		self.register_hooks()
		
		self.channels = {}
		
	def set_attribute(self, key, value):
		if key == 'port':
			self.port = int(value)
		elif key == 'auto-join':
			self.autojoin = value
		elif key == 'oper-join':
			self.operjoin = value
		else:
			print "Config Error: Unrecognized directive: %s" % key

	def start(self):
		if not hasattr(self, 'name'):
			print "FAIL: name not set!"
			return
		
		self.endpoint = endpoints.TCP4ServerEndpoint(reactor, self.port)
		self.endpoint.listen(connection.IRCConnectionFactory(self))
		reactor.run()
		
	def register_hooks(self):
		for module in dir(modules):
			if module.startswith('__'): continue
			
			print "* loading module:", module
			
			# add the module's hook to the dictionary
			mod = sys.modules['modules.%s' % module]
			
			if not hasattr(mod, '__command__'):
				print "** FAIL: unable to load '%s' because __command__ is not set." % module
			
			self.hooks[mod.__command__] = mod.handle_event

	def register_client(self, ctcn):
		self.clients[ctcn.nick] = ctcn
		
		chan_modes = [symbols.status_modes[x]['modechar'] for x in sorted(symbols.status_modes, reverse=True)]
		chan_prefixes = [symbols.status_modes[x]['prefix'] for x in sorted(symbols.status_modes, reverse=True)]
		
		# send welcome info
		self.send_msg(ctcn, '001 %s :Welcome to %s, %s' % (ctcn.nick, self.name, ctcn.get_hostmask()))
		self.send_msg(ctcn, '002 %s :You host is %s, running GreenIRCDv0.1' % (ctcn.nick, self.name))
		self.send_msg(ctcn, '004 %s %s %s %s %s' % (ctcn.nick, self.name, self.version, ''.join(symbols.user_modes.keys()), ''.join(symbols.chan_modes.keys())))
		self.send_msg(ctcn, '005 %s PREFIX=(%s)%s :are supported' % (ctcn.nick, ''.join(chan_modes), ''.join(chan_prefixes)))
		
		# set initial client state
		# set modes
		setattr(ctcn, 'mode_stack', 0)
		#self.send_msg(ctcn, 'MODE %s :+i' % (ctcn.nick), ctcn.nick)
		# if there is any channels to autojoin, join them
		if len(self.autojoin) > 0:
			modules.join.handle_event(self, ctcn, [self.autojoin])

	def register_server(ctcn):
		self.servers.append(ctcn)
		
		return self
		
	def unregister_connection(self, ctcn):
		if hasattr(ctcn, 'nick') and ctcn.nick in self.clients: # a client lost connection
			# remove the user from all channels
			for chan in self.channels:
				channel = self.channels[chan]
				if ctcn in channel.members:
					channel.quit(ctcn)
			
			# remove the user from the server
			del self.clients[ctcn.nick]
			
		print "* client unregistered"
		
	def handle_message(self, ctcn, data):
		command = data.strip()
		msg = IRCMessage(command)
		
		self.do_command(ctcn, msg)
		
	def do_command(self, ctcn, msg):
		# attempt to handle the command with the correct hook module
		if msg.command.upper() in self.hooks:
			self.hooks[msg.command.upper()](self, ctcn, msg.params)

		
	def send_msg(self, ctcn, msg, prefix = None):
		ctcn.transport.write(':%s %s\r\n' % (self.name if (prefix == None) else prefix, msg))
	
	def send_numeric(self, ctcn, numeric, msg, prefix = None):
		self.send_msg(ctcn, '%s %s %s' % (numeric, ctcn.nick, msg), prefix)
		
	def announce(self, ctcn, msg, prefix = None, exclude = False):
		# send this message to every client we have registered
		for client in self.clients.values():
			if (not exclude) or (ctcn != client) or (not client.nick in self.clients):
				self.send_msg(client, msg, prefix)
			
	def announce_common(self, ctcn, msg, prefix = None, exclude = False):
		for chan in self.channels:
			if ctcn in self.channels[chan].members:
				self.announce_channel(ctcn, self.channels[chan], msg, prefix, exclude)

	def announce_channel(self, ctcn, channel, msg, prefix = None, exclude = False):
		# send this message to all members of a channel
		for user in channel.members:
			if (not exclude) or (user != ctcn) or (not user in self.clients.values()):
				self.send_msg(self.clients[user.nick], msg, prefix)		
		
class IRCMessage:
	def __init__(self, raw_msg = None):
		# parse raw_msg, if provided
		if raw_msg == None: return
		
		# first, split the command into its space-separated components
		components = raw_msg.split(' ')
		
		ptr = 0
		# first, determine the source of the message
		if(components[ptr].startswith(':')): # there is a prefix
			self.source = components[ptr][1:]
			print "Source:", self.source
			ptr = ptr + 1
		
		# then, parse the command
		self.command = components[ptr]
		print "Command:", self.command
		ptr = ptr + 1
		
		# next, parse the arguments
		# they are either trailing (following ':') or middle
		self.params = []
		for i in range(ptr, len(components)):
			if not components[i].startswith(':'):
				self.params.append(components[i])
			else: # trailing arguments
				self.params.append((' '.join(components[i:]))[1:])
				
		print "Params:", self.params
		
class OperEntry:
	def __init__(self, username, auth):
		self.username = username
		self.auth = auth
