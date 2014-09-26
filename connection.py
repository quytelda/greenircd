#
# connection.py - Host to peer socket connection abstraction
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

import socket, time
from twisted.internet import protocol, task
from twisted.protocols.basic import LineReceiver

import irc.connection
import modules.quit

FLOOD_CYCLE = 10
FLOOD_DELAY = 2
FLOOD_THRESHOLD = 5
FLOOD_KILL_THRESHOLD = 7

class Connection(LineReceiver):
	def __init__(self, server, ssl = False):

		# set connection properties
		self.host = {'ip' : None, 'hostname' : None}
		self.ssl = ssl
		self.server = server
		self.container = irc.connection.IRCConnection(server, self)
		self.alive = True
		self.floodcount = 0

		# start the livelihood check loop
		self.alive_timer = task.LoopingCall(self.check_alive)
		self.alive_timer.start(30)
		self.flood_timer = task.LoopingCall(self.reset_flood_count)
		self.flood_timer.start(FLOOD_CYCLE)


	def reset_flood_count(self):
		self.floodcount = 0


	def connectionMade(self):
		"""
		This hooks is triggered when a peer has initiated a connection to the server.
		Here the connection details (peer IP and hostname) are resolved.
		"""

		# determine the peer's address and hostname
		self.message('NOTICE AUTH :*** Connection established; finding your hostname...')
		self.host['ip'] = self.transport.getPeer().host
		try:
			self.host['hostname'] = socket.gethostbyaddr(self.host['ip'])[0]
			self.message('NOTICE AUTH :*** Found your hostname (%s).' % self.host['hostname'])
		except socket.herror:
			self.message('NOTICE AUTH :*** Unable to resolve host; using peer IP.')

		print '* connection established on port %s (%s)' % (self.transport.getHost().port, self.container.host(False))

	def connectionLost(self, reason):
		self.alive_timer.stop()
		print "* connection lost (%s)" % self.container.host(False)


	def lineReceived(self, data):
		"""
		Receives lines of data (separated by CR-LF) from the client, and passes them to the central server for processing
		via the connection's container object (which is or needs to be registered with the server).
		"""
		self.floodcount += 1

		if self.floodcount > FLOOD_THRESHOLD:
			time.sleep(FLOOD_DELAY)
		if self.floodcount > FLOOD_KILL_THRESHOLD:
			modules.quit.handle_event(self.server, self.container, ['Flood Protection'])

		self.container.handle_data(data)



	def check_alive(self):
		"""
		This method, called at regular intervals, checks to see if the client has sent any data (probably a PONG message)
		since the last PING message from the server.If not, the connection is considered dead and is terminated;
		otherwise, another PING message is sent.
		"""
		# if the last ping wasn't reciprocated, kill the connection
		# (generate a QUIT event with the appropriate reason)
		if not self.alive:
			print "!!!Client pinged out (%s)" % self.container.nick if hasattr(self.container, 'nick') else str(self)
			modules.quit.handle_event(self.server, self.container, ['Ping Timeout'])
			return

		print "!!!client still alive (%s)" % self.container.nick if hasattr(self.container, 'nick') else str(self)

		# ping the client anew
		# for some reason, the PING message should *not* be prefixed
		if isinstance(self.container, irc.client.IRCClient):
			self.alive = False
			self.transport.write("PING :%s\r\n" % self.server.name)
			print "!!!ping sent (%s)" % self.container.nick if hasattr(self.container, 'nick') else str(self)


	def message(self, msg, prefix = None):
		"""Sends a message to the client socket, appropriately prefixed and padded with the requisite CR-LF delimiter."""
		self.transport.write(":%s %s\r\n" % (prefix if (prefix != None) else self.server.name, msg))


	def numeric(self, numeric, nick, msg, prefix = None):
		"""
		Sends a properly formatted numeric message to the client.
		The message receives the proper prefix and CR-LF via connection.message().
		"""
		if nick != None:
			self.message("%03d %s %s" % (numeric, nick, msg), prefix)
		else:
			self.message("%03d %s" % (numeric, msg), prefix)



class ConnectionFactory(protocol.Factory):

	def __init__(self, server, ssl = False):
		self.server = server
		self.ssl = ssl


	def buildProtocol(self, addr):
		return Connection(self.server, self.ssl)
