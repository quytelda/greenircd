#
# kill.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

import modules.quit

__command__ = 'KILL'

def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.message("461 %s KILL :KILL takes at least 1 parameter!" % source.nick)
		return

	# only operators can use KILL
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	target = params[0]
	reason = params[1] if (len(params) > 1) else source.nick

	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		source.ctcn.message("401 %s :Nickname not in server database." % source.nick)
		return

	user = srv.clients[target]

	# can't kill protected users unless you have sufficient status
	if user.has_mode('q') and (source.mode_stack < symbols.user_modes['q']):
		source.ctcn.message("481 %s :You don't have permission to kill protected users." % source.nick)
		return

	# announce the kill notice
	# TODO what is XXX supposed to be?
	source.ctcn.message("KILL %s :XXX %s" % (user.nick, reason), source.hostmask())

	# create a quit event
	modules.quit.handle_event(srv, user, ['[%s] Local kill by %s (%s)' % (srv.name, source.nick, reason)])
