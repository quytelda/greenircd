#
# symbols.py
#

status_modes = {
	2**0 : {'prefix' : '', 'modechar' : ''},
	2**1 : {'prefix' : '+', 'modechar' : 'v'},
	2**2 : {'prefix' : '%', 'modechar' : 'h'},
	2**3 : {'prefix' : '@', 'modechar' : 'o'},
	2**4 : {'prefix' : '&', 'modechar' : 'a'},
	2**5 : {'prefix' : '~', 'modechar' : 'q'}
}

numeric = {
	'WELCOME' : '001'
}

# lvhopsmntikrRcaqOALQbSeIKVfMCuzNTGjZ
chan_modes = {
	'n' : 2**0,
	't' : 2**1,
	'l' : 2**2,
	'm' : 2**3,
	'P' : 2**4,
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
	'W' : 2**4
}

def parse_stack(stack, modes):
	mode_str = ''
	for mode in modes:
		if (stack & modes[mode]) > 0:
			mode_str += mode
	
	return mode_str
