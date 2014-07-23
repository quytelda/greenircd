# main.py - Generic container interface for peer connections
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

import socket

class IRCConnection:	
	def __init__(self, server, ctcn, primary = True):
		self.ctcn = ctcn
		self.server = server
		
		if primary:
			ctcn.container = self
	
	def handle_data(self, data):
		"""Passes the server the data from the connection.  In the future, this message should ensure that this is (a) allowed, and (b) valid."""
		# if data has been received, the connection is indeed alive
		# mark it alive, and reset the timer
		self.ctcn.alive = True
		#self.ctcn.alive_timer.reset()
		print "!!!Data received (%s), client is alive (%s)" % (data, self.nick if hasattr(self, 'nick') else str(self))

		self.server.handle_message(self, data)
		
	# TODO implement cloaking
	def host(self, cloak = True):
		rhost = self.ctcn.host['hostname'] if (self.ctcn.host['hostname'] != None) else self.ctcn.host['ip']
		return rhost

	def terminate(self):
		self.ctcn.transport.loseConnection()
