#
# irc/client.py
#

import irc
import symbols
import hashlib

class IRCClient(irc.connection.IRCConnection):
	nick = None
	username = None
	vhost = None
	real_name = None
	mode_stack = 0
	away = False

	def __init__(self, server, ctcn, username, nick = None):
		irc.connection.IRCConnection.__init__(self, server, ctcn)
		self.username = username
		self.nick = nick

	def host(self, cloak = True):
		rhost = self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']
		if self.has_mode('t') and (vhost != None):
			return vhost
		elif self.has_mode('x') and cloak:
			return self.gencloak(rhost)
		else:
			return rhost

	def gencloak(self, h, full = False):
		elems = h.split('.')
		for i in range(0, len(elems)):
			elems[i] = hashlib.sha256(elems[i]).hexdigest()[:len(elems[i])]
			
		return '.'.join(elems)

	def hostmask(self, cloak = True):
		return "%s!%s@%s" % (self.nick, self.username, self.host(cloak))

	# convenience method to test if a user has a mode flag set
	def has_mode(self, flag):
		return (self.mode_stack & symbols.user_modes[flag]) > 0
