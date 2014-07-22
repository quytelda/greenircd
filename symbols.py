# symbols.py - GreenIRCd symbol definitions
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WeeChat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

# TODO: chanmodes +pbki, usermodes +si

CHOWNER = 2**5
CHADMIN = 2**4
CHOPER = 2**3
CHHOP = 2**2
CHVOICE = 2**1
CHUSER = 2**0

# Numeric replies defined in the RFC for the IRC protocol
RPL_WELCOME = 001
RPL_YOURHOST = 002
RPL_MYINFO = 004
RPL_ISUPPORT = 005
RPL_UMODEIS = 221 # <user_modes> [<user_mode_params>]
RPL_ADMINME = 256 # <server> :<info>
RPL_ADMINEMAIL = 259 # :<email>
RPL_AWAY = 301
RPL_UNAWAY = 305 # :<info>
RPL_NOWAWAY = 306 # :<info>
RPL_WHOISUSER = 311 # <nick> <user> <host> * :<real_name>
RPL_WHOISSERVER = 312 # <nick> <server> :<server_info>
RPL_WHOISOPERATOR = 313 # <nick> :priveleges
RPL_WHOWASUSER = 314
RPL_ENDOFWHO = 315 # <name> :<info>
RPL_ENDOFWHOIS = 318
RPL_WHOISCHANNELS = 319
RPL_LISTSTART = 321 # Channels :Users Name
RPL_LIST = 322 # <channel> <#_visible> :<topic>
RPL_LISTEND = 323 # :info
RPL_CHANNELMODEIS = 324 # <channel> <mode> <mode_params>
RPL_TOPIC = 332 # <channel> :<topic>
RPL_WHOREPLY = 352 # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
RPL_NAMREPLY = 353 # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
RPL_ENDOFNAMES = 366 # <channel> :<info>
RPL_REHASHING = 382 # <config_file> :<info>
ERR_NOSUCHNICK = 401 # <nick> :<reason>
ERR_NOSUCHCHANNEL = 403 # <channel> :<reason>
ERR_CANNOTSENDTOCHAN = 404 # <channel> :<reason>
ERR_NONICKNAMEGIVEN = 431
ERR_NICKNAMEINUSE = 433 # <nick> :<reason>
ERR_NOTREGISTERED = 451 # :<reason>
ERR_NEEDMOREPARAMS = 461 # <command> :<reason>
ERR_ALREADYREGISTERED = 462 # :<reason>
ERR_CHANNELISFULL = 471 # <channel> :<reason>
ERR_NOPRIVILEGES = 481 # :<reason>

# channel management status modes
status_modes = {
	CHUSER : {'prefix' : '', 'modechar' : ''},
	CHVOICE : {'prefix' : '+', 'modechar' : 'v'},
	CHHOP : {'prefix' : '%', 'modechar' : 'h'},
	CHOPER : {'prefix' : '@', 'modechar' : 'o'},
	CHADMIN : {'prefix' : '&', 'modechar' : 'a'},
	CHOWNER : {'prefix' : '~', 'modechar' : 'q'}
}

# channel mode symbols and masks
chan_modes = {
	'n' : 2**0, # no outside messages
	't' : 2**1, # restricted topic changes
	's' : 2**2, # secret channel (unlisted)
	'l' : 2**3, # channel size limit (takes integer param)
	'm' : 2**4, # moderated
	'P' : 2**5, # persistant ops
	'Z' : 2**6, # SSL users only
	'O' : 2**7, # server operators only
	'A' : 2**8, # administrators only

	# channel status modes
	# since these modes affect the status of individual users in the channel
	# they have a mask of zero, since it isn't a toggleable setting
	'v' : 0, # voiced 
	'h' : 0, # half operator
	'o' : 0, # operators
	'a' : 0, # administrator
	'q' : 0  # owner
}

# user mode symbols and masks
user_modes = {
	# "freely settable" modes
	'i' : 2**0, # invisible
	'x' : 2**1, # cloaked host
	'w' : 2**2, # receives Wallops
	'p' : 2**4, # hides channels
	's' : 2**5, # receives server notices
	
	# restricted modes
	'z' : 2**6, # using SSL
	't' : 2**7, # using vhost
	'r' : 2**8, # registered
	'S' : 2**9,  # network service
	
	# operator modes
	'o' : 2**10, # local operator
	'O' : 2**11, # global operator
	'q' : 2**12, # protected
	'Q' : 2**13, # can override
	'a' : 2**14, # local administrator
	'A' : 2**15 # network administrator
}

def parse_stack(stack, modes):
	mode_str = ''
	for mode in modes:
		if (stack & modes[mode]) > 0:
			mode_str += mode
	
	return mode_str
