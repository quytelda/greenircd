#
# symbols.py
#

CHOWNER = 2**5
CHADMIN = 2**4
CHOPER = 2**3
CHHOP = 2**2
CHVOICE = 2**1
CHUSER = 2**0

RPL_WELCOME = 001
RPL_AWAY = 301
RPL_WHOISUSER = 311 # <nick> <user> <host> * :<real_name>
RPL_WHOISSERVER = 312 # <nick> <server> :<server_info>
RPL_WHOISOPERATOR = 313 # <nick> :priveleges
RPL_WHOWASUSER = 314
RPL_ENDOFWHOIS = 318
RPL_WHOISCHANNELS = 319
RPL_LISTSTART = 321 # Channels :Users Name
RPL_LIST = 322 # <channel> <#_visible> :<topic>
RPL_LISTEND = 323 # :info
RPL_NAMREPLY = 353 # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
RPL_ENDOFNAMES = 366 # <channel> :<info>
ERR_NOSUCHNICK = 401 # <nick> :*( ( '@' / '+' ) <channel> ' ' )
ERR_NOSUCHCHANNEL = 403 # <channel> :<reason>
ERR_NONICKNAMEGIVEN = 431
ERR_NEEDMOREPARAMS = 461 # <command> :<reason>

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
	'o' : 2**3,
	'W' : 2**4,
	'q' : 2**5,
	'a' : 2**10
}

def parse_stack(stack, modes):
	mode_str = ''
	for mode in modes:
		if (stack & modes[mode]) > 0:
			mode_str += mode
	
	return mode_str
