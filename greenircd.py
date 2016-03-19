#!/usr/bin/python

#
# main.py - Primary entry point for GreenIRCd software
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

import sys
from twisted.internet import ssl, reactor

from lib.connection import ConnectionFactory
from lib.server import Server

def arg_matches(arg, short, long = None):
	return (arg == short) or (arg == long)


def main(argv):
	"""
	:param argv Command line options

	Primary entry point function; initializes and starts the program.
	"""

	server = Server('greenircd')
	factory = ConnectionFactory(server)
	reactor.listenTCP(6667, factory)
	reactor.run()


if __name__ == "__main__":
	main(sys.argv)
