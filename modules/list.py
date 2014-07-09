#
# list.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'LIST'

# LIST [<channel>{,<channel>} [<server>]]
def handle_event(srv, ctcn, params):
	# send the list header
	srv.send_numeric(ctcn, symbols.RPL_LISTSTART, 'Channels :Users Name')
	
	# for each channel send the LIST info
	for channel in srv.channels.values():
		if channel.has_mode('s'): continue
		srv.send_numeric(ctcn, symbols.RPL_LIST, '%s %s :%s' % (channel.name, len(channel.members), channel.topic))
	
	# send the RPL_ENDLIST to signify the finish
	srv.send_numeric(ctcn, symbols.RPL_LISTEND, ':End of LIST list.')
