#
# module.py
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

class Module(object):

	def __init__(self, server):
		self._server = server

	def __message_client(self, nick, prefix, command, params):
		self._server.message_client(nick, prefix, command, params)

	def __message_channel(self, target, prefix, command, params):
		self._server.message_channel(nick, prefix, command, params)

	def __send_numeric(self, target, prefix, command, params):
		self._server.numeric(target, prefix, command, params)
