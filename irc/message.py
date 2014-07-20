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
				break
				
		print "Params:", self.params
