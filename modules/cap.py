#
# cap.py
# Copyright (C) 2014 Quytelda Gaiwin
#

import symbols

__command__ = "KICK"

def handle_event(srv, source, params):
	if len(params) < 1:
		return

	cmd = params[0]
	if cmd == "LS":
		source.ctcn.message("CAP * LS :multi-prefix")

