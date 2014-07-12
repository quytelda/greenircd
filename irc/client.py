#
# irc/client.py
#

import irc
import symbols

class IRCClient(irc.connection.IRCConnection):
	nick = None
	username = None
	vhost = None
	mode_stack = 0
	away = False

	def __init__(self, server, ctcn, username, nick = None):
		irc.connection.IRCConnection.__init__(self, server, ctcn)
		self.username = username
		self.nick = nick

	def userhost(self, cloak = True):
		if self.has_mode('t') and (vhost != None):
			return
		elif self.has_mode('x') and cloak:
			return
		else:
			return self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']

	def hostmask(self, cloak = True):
		return "%s!%s@%s" % (self.nick, self.username, self.userhost(cloak))

	# convenience method to test if a user has a mode flag set
	def has_mode(self, flag):
		return (self.mode_stack & symbols.user_modes[flag]) > 0
