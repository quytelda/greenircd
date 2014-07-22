#
# whois.py - IRC WHOIS message handler
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

__command__ = 'WHOIS'

# WHOIS Syntax: WHOIS [<server>] <nickmask>[,<nickmask>[,...]]
def handle_event(srv, source, params):
	# make sure there are sufficient parameters
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NONICKNAMEGIVEN, source.nick, "%s WHOIS :The WHOIS command requires one parameter!" % source.nick)
		return
	target = params[0]
	
	# the target must be registered
	if not target in srv.clients:
		source.ctcn.numeric(symbols.ERR_NOSUCHNICK, source.nick, "%s :Nickname not in server database." % source.nick)
		return
	
	user = srv.clients[target]
	
	cloak = not (source.has_mode('o') or user == source)
	
	# send the information summary
	source.ctcn.numeric(symbols.RPL_WHOISUSER, source.nick, "%s %s %s * :%s" % (user.nick, user.username, user.host(cloak), user.real_name))
	source.ctcn.numeric(symbols.RPL_WHOISSERVER, source.nick, "%s %s :%s" % (user.nick, user.server.name, srv.info))
	
	chans = []
	
	# gather a list of channels to send for the RPL_WHOISCHANNELS message
	# each channel is prefixed with the appropriate status prefix (if applicable)
	for chan in srv.channels:
		if user in srv.channels[chan].members: chans.append(srv.channels[chan].prefix(user)[:1] + chan)
	
	if len(chans) > 0:
		source.ctcn.numeric(symbols.RPL_WHOISCHANNELS, source.nick, "%s :%s" % (user.nick, ' '.join(chans)))
	
	if user.has_mode('A'):
		source.ctcn.numeric(symbols.RPL_WHOISOPERATOR, source.nick, "%s :is a global administrator" % user.nick)
	elif user.has_mode('a'):
		source.ctcn.numeric(symbols.RPL_WHOISOPERATOR, source.nick, "%s :is a server administrator" % user.nick)
	elif user.has_mode('O'):
		source.ctcn.numeric(symbols.RPL_WHOISOPERATOR, source.nick, "%s :is a global operator" % user.nick)	
	elif user.has_mode('o'):
		source.ctcn.numeric(symbols.RPL_WHOISOPERATOR, source.nick, "%s :is a server operator" % user.nick)

	source.ctcn.numeric(symbols.RPL_ENDOFWHOIS, source.nick, "%s :END OF WHOIS" % user.nick)
