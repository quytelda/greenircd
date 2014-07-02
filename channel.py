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
	
	def __init__(self, name, server):
		self.name = name
		self.server = server
		self.topic = ''
		self.modes = ''
		self.mode_stack = 0
		self.members = {}
	
	def join(self, user):
		# the first user gets the highest mode available (+q, owner)
		status = symbols.status_modes.keys()[0] if (len(self.members) == 0) else 0
		self.members[user] = status
	
	def part(self, user):
		del self.members[user]
		
	def quit(self, user):
		del self.members[user]

	def add_mode(self, flag, params = []):
		mask = symbols.chan_modes[flag] # get the corresponding mask
		
		# deal with status modes
		if (mask == 0) and (len(params) > 0) and (params[0] in self.server.clients):
			target = params[0]
			print "setting +%s on %s in %s" % (flag, target, self.name)
			
			# look up the mode
			for status in symbols.status_modes.items():
				if status[1]['modechar'] == flag:
					self.members[self.server.clients[params[0]]] |= status[0]
					
		# apply the mask to the channel mode
		self.mode_stack |= mask
		
	def rem_mode(self, flag, params = None):
		mask = symbols.chan_modes[flag] # get the corresponding mask

		# deal with status modes
		if (mask == 0) and (len(params) > 0) and (params[0] in self.server.clients):
			target = params[0]
			print "setting-%s on %s in %s" % (flag, target, self.name)
			
			# look up the mode
			for status in symbols.status_modes.items():
				if status[1]['modechar'] == flag:
					self.members[self.server.clients[params[0]]] ^= status[0]
		
		# apply the mask to the channel mode
		self.mode_stack ^= mask

	def topic(self, caller, new_topic):
		self.topic = new_topic

	def has_mode(self, flag):
		return (self.mode_stack & symbols.chan_modes[flag]) > 0
		
	def get_status(self, user):
		highest_status = 1
		for mode in symbols.status_modes:
			if (self.members[user] & mode) > highest_status: highest_status = mode
		
		print "* detected user had status", symbols.status_modes[highest_status]['prefix']
		
		return highest_status
		
	def names(self):
		nam_list = ''
		for member in self.members:
			status = self.get_status(member)
			nam_list = nam_list + ' ' + symbols.status_modes[status]['prefix'] + member.nick
			
		return nam_list.strip()
