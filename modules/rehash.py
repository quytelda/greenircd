#
# rehash.py - IRC REHASH message handler
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

import symbols

import config

__command__ = 'REHASH'

def handle_event(srv, source, params):
	# only operators can use REHASH
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	# announce the rehash
	# TODO what is XXX supposed to be?
	source.ctcn.numeric(symbols.RPL_REHASHING, source.nick, "%s :Rehashing config file..." % srv.config)
	config.config(srv, srv.config)
	source.ctcn.numeric(symbols.RPL_REHASHING, source.nick, "%s :Sucessfully rehashed %s" % (srv.config, srv.name))
