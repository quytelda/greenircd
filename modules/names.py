#
# names.py
#

import symbols

__command__ = "NAMES"

# NAMES Syntax: NAMES <channel>{,<channel>}
def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick, "NAMES :NAMES requires at least one parameter.")
		return
	target = params[0]

	# there may be a comma separated list of channels
	# if so, rerun this method for each channel in the list
	if ',' in target:
		for chan in target.split(','): handle_event(srv, source, [chan])
		return

	# the channel must exist
	if not target in srv.channels:
		source.ctcn.numeric(symbols.ERR_NOSUCHCHANNEL, source.nick, "%s :No such channel." % target)
		return
	channel = srv.channels[target]

	# generate a list
	names = ''
	for member in channel.members:
		names += channel.prefix(member) + member.nick + ' '

	names = names.strip()

	source.ctcn.numeric(symbols.RPL_NAMREPLY, source.nick, "= %s :%s" % (target, names))
	source.ctcn.numeric(symbols.RPL_ENDOFNAMES, source.nick, "%s :End of NAMES list" % target)
