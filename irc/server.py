#
# irc/server.py
#

import irc

class IRCServer(irc.connection.IRCConnection):
	def __init__(self):
		self.ulined = False
