#
# irc/server.py
#

import irc

class IRCServer(irc.connection.IRCConnection):
	def __init__(self, ctcn, name, hops, info):
		self.ctcn = ctcn
		self.name = name
		self.hops = int(hops) #TODO value checking
		self.info = info
		self.ulined = False
