#
# channel.py - Definition for channel object and methods
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WeeChat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

import symbols
		
class IRCChannel:
	"""
	IRCChannel represents an IRC channel (by its collection of users and properties) on the network.
	"""

	def __init__(self, name, server):
		self.name = name
		self.server = server
		self.mode_stack = 0
		self.topic = ''
		self.limit = 30
		self.members = {}
		self.bans = []


	def join(self, client):
		"""
		Adds a client as a member in the channel.  If they are the first, they get ops (+qo).
		This method does /not/ generate or represent JOIN event (a JOIN event will likely invoke this if succesful)
		"""
		# the first user gets the highest mode available (+q, owner)
		# we will apply +qo to the user automatically, since many clients put more emphasis on operators
		status = (symbols.CHOWNER | symbols.CHOPER) if (len(self.members) == 0) else 1
		self.members[client] = status


	def part(self, client):
		"""
		Removes a user from a channel. If the client isn't in the channel, it is ignored.
		This method does /not/ represent a PART event.
		"""
		if client in self.members:
			del self.members[client]
			
		# if it was the last channel, remove it
		if (len(self.members) < 1) and (self.name in self.server.channels):
			del self.server.channels[self.name]


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


	def is_banned(self, user):
		"""Checks if a user is banned from this channel."""
		#TODO implement wildcards
		
		return user.hostmask() in self.bans
