#
# names.py
#

import symbols

__command__ = "NAMES"

# NAMES Syntax: NAMES <channel>{,<channel>}
def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_numeric(ctcn, symbols.ERR_NEEDMOREPARAMS, "NAMES :NAMES requires at least one parameter.")
		return
	target = params[0]
	
	# there may be a comma separated list of channels
	# if so, rerun this method for each channel in the list
	if ',' in target:
		for chan in target.split(','): handle_event(srv, ctcn, [chan])
		return
	
	# the channel must exists
	if not target in srv.channels:
		srv.send_numeric(ctcn, symbols.ERR_NOSUCHCHANNEL, "%s :No such channel." % target)
		return
	channel = srv.channels[target]
	
	# generate a list
	names = ''
	for member in channel.members:
		names += channel.prefix(member) + member.nick + ' '

	names = names.strip()
	
	srv.send_numeric(ctcn, symbols.RPL_NAMREPLY, "= %s :%s" % (target, names))
	srv.send_numeric(ctcn, symbols.RPL_ENDOFNAMES, "%s :%s" % (target, "End of NAMES List"))
