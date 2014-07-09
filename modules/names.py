#
# names.py
#

import symbols

__command__ = "NAMES"

# NAMES Syntax: NAMES <channel>{,<channel>}
def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_numeric(ctcn, symbols.ERR_NEEDMOREPARAMS, "NAMES :NAMES requires at least one parameter.")

	chan = params[0]
	
	channel = srv.channels[chan]
	
	# generate a list
	names = ''
	for member in channel.members:
		names += channel.prefix(member) + member.nick + ' '
	
	names = names.strip()
	
	srv.send_numeric(ctcn, symbols.RPL_NAMREPLY, "= %s :%s" % (chan, names))
	srv.send_numeric(ctcn, symbols.RPL_ENDOFNAMES, "%s :%s" % (chan, "End of NAMES List"))
