#
# oper.py
#

import symbols

__command__ = 'OPER'


def handle_event(self, ctcn, params):
	username = params[0]
	password = params[1]
	
	# authenticate the user
	if (username != 'quytelda') and (password != 'OperPassword!'): return
	
	for m in symbols.oper_modes:
		ctcn.add_mode(m)
	
	self.send_msg(ctcn, 'MODE %s :+%s' % (ctcn.nick, symbols.oper_modes), ctcn.nick)
	self.send_msg(ctcn, '381 %s :%s' % (ctcn.nick, '*** Logged in as IRC Operator'))
