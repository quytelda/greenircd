#
# channel.py
# Copyright (C) 2014 Quytelda Gaiwin
#

import symbols

import modules.mode

# 
# IRCChannel
# This class represents an IRC channel
#			
class IRCChannel:
	
	def __init__(self, name, server):
		self.name = name
		self.server = server
		self.topic = ''
		self.modes = ''
		self.mode_stack = 0
		self.limit = 30
		self.members = {}
	
	def join(self, user):
		# the first user gets the highest mode available (+q, owner)
		status = (symbols.CHOWNER | symbols.CHOPER) if (len(self.members) == 0) else 1
		self.members[user] = status
	
	def part(self, user):
		# if the channel has the persistant op (+P) flag set
		# and this is the last op, op the first member
		if self.has_mode('P') and (len(self.members) > 1) and any(self.members[member] < 2**3 for member in self.members):
			new_op = None
			# find the best candidate to receive ops
			for member in self.members:
				if (user != member) and (new_op == None or self.members[new_op] < self.members[member]):
					new_op = member

			# generate mode change event
			modules.mode.handle_event(self.server, user, [self.name, '+o', new_op.nick])
	
		del self.members[user]
		
	def quit(self, user):
		del self.members[user]

	def topic(self, caller, new_topic):
		self.topic = new_topic

	def has_mode(self, flag):
		return (self.mode_stack & symbols.chan_modes[flag]) > 0
		
	def get_status(self, user):
		highest_status = 1
		for mode in symbols.status_modes:
			if (self.members[user] & mode) > highest_status: highest_status = mode
		
		return highest_status
	
	def prefix(self, user):
		prefix = ''
		for status in sorted(symbols.status_modes, reverse = True):
			if (self.members[user] & status) > 0:
				prefix += symbols.status_modes[status]['prefix']
				
		return prefix

	def names(self):
		nam_list = ''
		for member in self.members:
			status = self.get_status(member)
			nam_list = nam_list + ' ' + symbols.status_modes[status]['prefix'] + member.nick
			
		return nam_list.strip()
