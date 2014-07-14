#
# symbols.py
#

# TODO: chanmodes +pbki, usermodes +si

CHOWNER = 2**5
CHADMIN = 2**4
CHOPER = 2**3
CHHOP = 2**2
CHVOICE = 2**1
CHUSER = 2**0

RPL_WELCOME = 001
RPL_YOURHOST = 002
RPL_MYINFO = 004
RPL_ISUPPORT = 005
RPL_UMODEIS = 221 # <user_modes> [<user_mode_params>]
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

status_modes = {
	CHUSER : {'prefix' : '', 'modechar' : ''},
	CHVOICE : {'prefix' : '+', 'modechar' : 'v'},
	CHHOP : {'prefix' : '%', 'modechar' : 'h'},
	CHOPER : {'prefix' : '@', 'modechar' : 'o'},
	CHADMIN : {'prefix' : '&', 'modechar' : 'a'},
	CHOWNER : {'prefix' : '~', 'modechar' : 'q'}
}

# lvhopsmntikrRcaqOALQbSeIKVfMCuzNTGjZ
chan_modes = {
	'n' : 2**0,
	't' : 2**1,
	'l' : 2**2,
	'm' : 2**3,
	'P' : 2**4,
	'O' : 2**5,
	's' : 2**6,
	'o' : 0,
	'v' : 0,
	'h' : 0,
	'a' : 0,
	'q' : 0
}

user_modes = {
	'i' : 2**0,
	'x' : 2**1,
	'w' : 2**2,
	't' : 2**3,
	'o' : 2**4,
	'W' : 2**5, # XXX I don't like this one
	'q' : 2**6,
	'a' : 2**10
}

def parse_stack(stack, modes):
	mode_str = ''
	for mode in modes:
		if (stack & modes[mode]) > 0:
			mode_str += mode
	
	return mode_str
