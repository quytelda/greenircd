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
		print "** JOIN:", user
		print "members:", self.members
		status = 3 if (len(self.members) == 0) else 0
		self.members[user] = status
	
	def part(self, user):
		del self.members[user]
		
	def quit(self, user):
		del self.members[user]
	
	# when a mode is set on the channel, the server calls this method
	# to apply the mode to channel.  I returns the actual net mode-change applied
	def set_mode(self, caller, modes, param = None):
		# make sure the user is an operator
		if not self.members[caller] >= 3: return
		
		# first, we need to save the original mode stack,
		# so we can easily calculate the difference later
		original_modes = self.mode_stack
		
		# parse the mode change
		if '+' in modes: # we will add modes
			ptr = modes.index('+') + 1
			while (ptr < len(modes)) and (modes[ptr] != '-'):
				# flag for is the mode was handled
				handled = False
				
				# first, we deal with status modes
				# check if this mode is a channel status mode
				# each status in the iteration is a tuple (modevalue # (int), {'prefix', 'modechar'}
				for status in symbols.chan_status_modes.items():
				
					# if we didn't find it, check the next one
					if(status[1]['modechar'] != modes[ptr]): continue
				
					# if there's no parameter, give up
					if(param == None):
						break
					
					# if we have a member by the name in param, set its status
					for user in self.members:
						if user.nick == param: # we found a match, so set it's mode
							self.members[user] = status[0]
							break
					else: # the user isn't in this channel
						break
					
					# we have already taken care of things, continue
					handled = True
					
				# if we've already handled this mode char, move on to the next
				if handled:
					ptr += 1
					continue
			
				mode = modes[ptr] # get the current mode char
				mode_mask = symbols.chan_modes[mode] # get the corresponding mask
				
				# apply the mask to the channel mode
				self.mode_stack |= mode_mask
				print "* mode_stack changed to ", self.mode_stack
				
				# increment to the next mode char
				ptr += 1
		
		# return the modes /actually/ applied
		return (self.mode_stack ^ original_modes)
		
	def add_mode(self, flag, params = []):
		mask = symbols.chan_modes[flag] # get the corresponding mask
		
		# deal with status modes
		if (mask == 0) and (params != []) and (params[0] != ''):
			target = params[0]
			print "setting +%s on %s in %s" % (flag, target, self.name)
			
			# look up the mode
			for status in symbols.chan_status_modes.items():
				if status[1]['modechar'] == flag:
					self.members[self.server.clients[params[0]]] = status[0]
					
		# apply the mask to the channel mode
		self.mode_stack |= mask
		print "* mode_stack changed to ", self.mode_stack
		
	def rem_mode(self, flag, params = None):
		mask = symbols.chan_modes[flag] # get the corresponding mask

		# deal with status modes
		if (mask == 0) and (params != []) and (params[0] != ''):
			target = params[0]
			print "setting-%s on %s in %s" % (flag, target, self.name)
			
			# look up the mode
			for status in symbols.chan_status_modes.items():
				if status[1]['modechar'] == flag:
					self.members[self.server.clients[params[0]]] = 0	
		
		# apply the mask to the channel mode
		self.mode_stack ^= mask
		print "* mode_stack changed to ", self.mode_stack

	def topic(self, caller, new_topic):
		self.topic = new_topic

	def has_mode(self, flag):
		return (self.mode_stack & symbols.chan_modes[flag]) > 0
			
	def names(self):
		nam_list = ''
		for member in self.members:
			status = self.members[member]
			nam_list = nam_list + ' ' + symbols.chan_status_modes[status]['prefix'] + member.nick
			
		return nam_list.strip()
