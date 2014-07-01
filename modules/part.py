#
# part.py
#

__command__ = 'PART'

def handle_event(srv, ctcn, params):
	# die if there are no parameters
	if len(params) < 1: return
	target = params[0]
	msg = "Leaving" if (len(params) < 2) else params[1]
	
	# if the channel doesn't exist, ignore
	if not (target in srv.channels): return
	channel = srv.channels[target]
	
	# if the user is not in the channel, ignore
	if not ctcn in channel.members: return

	# send announcement, and confirmation
	srv.announce_channel(ctcn, channel, 'PART %s :%s' % (target, msg), ctcn.get_hostmask())
	
	# part the user
	channel.part(ctcn)
