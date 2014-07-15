#
# admin.py
#

import symbols

__command__ = 'ADMIN'

def handle_event(srv, source, params):
	source.ctcn.notice(symbols.RPL_ADMINME, source.nick, '%s :Administrative Information about %s', (srv.name, srv.name))
	
	source.ctcn.notice(symbols.RPL_ADMINEMAIL, source.nick, ':' + srv.admin_email)
