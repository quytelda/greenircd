# client.py - Container for client connections
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
# GreenIRCd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

import irc
import symbols
import hashlib

class IRCClient(irc.connection.IRCConnection):

	def __init__(self, server, ctcn, username, nick = None):
		irc.connection.IRCConnection.__init__(self, server, ctcn)
		self.vhost = None
		self.real_name = None
		self.mode_stack = 0
		self.away = False
		self.away_reason = None
		self.username = username
		self.nick = nick

	def host(self, cloak = True):
		rhost = self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']
		if self.has_mode('t') and (self.vhost != None):
			return self.vhost
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
