#
# list.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'LIST'

# LIST [<channel>{,<channel>} [<server>]]
def handle_event(srv, source, params):
	# send the list header
	source.ctcn.numeric(symbols.RPL_LISTSTART, source.nick, 'Channels :Users Name')
	
	# for each channel send the LIST info
	for channel in srv.channels.values():
		if channel.has_mode('s'): continue
		mode_string = symbols.parse_stack(channel.mode_stack, symbols.chan_modes)
		source.ctcn.numeric(symbols.RPL_LIST, source.nick, '%s %s :[+%s] %s' % (channel.name, len(channel.members), mode_string, channel.topic))
	
	# send the RPL_ENDLIST to signify the finish
	source.ctcn.numeric(symbols.RPL_LISTEND, source.nick, ':End of LIST list')
