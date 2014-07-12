#
# channel.py
# Copyright (C) 2014 Quytelda Gaiwin
#

import symbols

# 
# IRCChannel
# This class represents an IRC channel
#			
class IRCChannel:
	name = None
	mode_stack = 0
	topic = ''
	limit = 30
	members = {}

	def __init__(self, name):
		self.name = name
	
	def join(self, client):
		"""Adds a client as a member in the channel.  If they are the first, they get ops (+qo)."""
		# the first user gets the highest mode available (+q, owner)
		# we will apply +qo to the user automatically, since many clients put more emphasis on operators
		status = (symbols.CHOWNER | symbols.CHOPER) if (len(self.members) == 0) else 1
		self.members[client] = status
	
	def part(self, client):
		"""Removes a user from a channel. If the client isn't in the channel, it is ignored."""
		if client in self.members:
			del self.members[client]

	def has_mode(self, flag):
		"""Convenience method to check if the channel has a given mode flag enabled."""
		return (self.mode_stack & symbols.chan_modes[flag]) > 0

	def prefix(self, user):
		"""Returns the prefix of the user as it would appear in the names list; supports multi-prefix."""
		prefix = ''
		for status in sorted(symbols.status_modes, reverse = True):
			if (self.members[user] & status) > 0:
				prefix += symbols.status_modes[status]['prefix']
				
		return prefix

	def names(self):
		"""Returns a nicely formatted string for NAMES, with prefixes"""
		nam_list = ''
		for member in self.members:
			status = self.get_status(member)
			nam_list = nam_list + ' ' + symbols.status_modes[status]['prefix'] + member.nick
			
		return nam_list.strip()
