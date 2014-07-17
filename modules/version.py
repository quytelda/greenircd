#
# version.py
#

import symbols

__command__ = 'VERSION'

def handle_event(srv, source, params):
	# generate the sorted list of modechars and corresponding prefixes
	chan_modes = [symbols.status_modes[x]['modechar'] for x in sorted(symbols.status_modes, reverse=True)]
	chan_prefixes = [symbols.status_modes[x]['prefix'] for x in sorted(symbols.status_modes, reverse=True)]

	# send the expected numeric replies
	source.ctcn.numeric(symbols.RPL_YOURHOST, source.nick,
		':Your host is %s, running version %s' % (srv.name, srv.version))
	source.ctcn.numeric(symbols.RPL_MYINFO, source.nick,
		'%s %s %s %s' % (srv.name, srv.version, ''.join(symbols.user_modes.keys()), ''.join(symbols.chan_modes.keys())))
	source.ctcn.numeric(symbols.RPL_ISUPPORT, source.nick,
		'PREFIX=(%s)%s CHANTYPES=# :are supported' % (''.join(chan_modes), ''.join(chan_prefixes)))