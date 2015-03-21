#
# channel.py - Relay chat channel representation
#
# Copyright (C) 2015 Quytelda Kahja <quytelda@tamalin.org>
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

class Channel(object):

	__cmodes = {
		'n' : 0,
		't' : 1,
		's' : 2
	}

	__smodes = {
		'o' : 0,
		'q' : 1
	}

	DEFAULT_SMODE = 0
	FIRST_JOIN_SMODE = 1

	__prefixes = {
		'o' : '@',
		'q' : '~'
	}

	def __init__(self, name, modes = 0):
		self.name = name
		self.modes = modes

		self.members = {}


	def mode(self, enable, mode, param = None):

		# lookup mode
		if mode not in self.__cmodes:
			return
		mode_mask = self.__cmodes[mode]

		if enable:
			self.__set_cmode(mode_mask, param)
		else:
			self.__unset_cmode(mode_mask, param)


	def __set_cmode(self, mode, param = None):
		self.modes |= (2**mode)


	def __unset_cmode(self, mode, param = None):
		self.modes &= ~(2**mode)


	def join(self, nick):

		# ignore redundant joins
		if nick in self.members:
			return

		# first to join gets special modes
		if len(self.members) == 0:
			self.members[nick] = self.FIRST_JOIN_SMODE
		else:
			self.members[nick] = self.DEFAULT_SMODE
