#
# list.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'LIST'

def handle_event(srv, ctcn, params):
	for chan in srv.channels:
		srv.send_msg(ctcn, '321 Channels :Users Name')
		srv.send_msg(ctcn, '322 %s %s %s :%s' % (ctcn.nick, chan, len(srv.channels[chan].members), srv.channels[chan].topic))
		srv.send_msg(ctcn, '323 :End of LIST list')
