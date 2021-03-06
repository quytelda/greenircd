#
# error.py - Errors
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

class NoSuchTargetError(Exception):

	def __init__(self, target):
		self.target = target

	def __str__(self):
		return "Unknown target: %s" % self.target


class NameInUseError(Exception):

	def __init__(self, name, ctcn = None):
		self.name = name
		self.ctcn = ctcn

	def __str__(self):
		return "Unknown target: %s" % self.name
