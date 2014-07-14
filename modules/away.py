#
# away.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'AWAY'

# Syntax: AWAY [<reason>]
def handle_event(srv, source, params):
	# if a reason is provided, we set away to True
	if len(params) > 0:
		source.away = True
		source.away_reason = params[0]
		source.ctcn.numeric(symbols.RPL_NOWAWAY, source.nick, ":You are now marked as away.")
	elif source.away:
		source.away = False
		source.ctcn.numeric(symbols.RPL_UNAWAY, source.nick, ":You are no longer marked as away.")
