#
# part.py
#

import mode

__command__ = 'PART'

def handle_event(srv, source, params):
	# die if there are no parameters
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick, "PART :PART takes at least 1 parameters!")
		return

	target = params[0]
	msg = "Leaving" if (len(params) < 2) else params[1]

	# if the channel doesn't exist, ignore
	if not (target in srv.channels):
		return

	channel = srv.channels[target]

	# if the user is not in the channel, ignore
	if not source in channel.members: return

	# send announcement, and confirmation
	srv.announce_channel(channel, 'PART %s :%s' % (target, msg), source.hostmask())

	# part the user
	channel.part(source)
	
	# if that was the last user in the channel, we should forget the channel
	# TODO
