#
# module.py
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

def min_params(num):
	"""
	A python decorator that checks whether enough arguments were passed
	to run the command handler.
	"""
	def min_params_decorator(handler):
		def wrapper(self, source, message):
			if len(message['params']) >= num: handler(self, source, message)
		return wrapper
	return min_params_decorator

class Module(object):

	def __init__(self, server):
		self.server = server


	def handle_unreg(self, source, message):
		pass


	def handle_client(self, source, message):
		pass


	def handle_server(self, source, message):
		pass
