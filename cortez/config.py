import configparser

CLIENT_ID = "a1a76b5205bb80d8f7ad182133028016"
CLIENT_SECRET = '3e027a923d14d7e64bee792643dd23f2'

def get_option():
	d = {}

	config = configparser.ConfigParser()
	config.read('config.cfg')

	options = config.options('cortez')

	for option in options:
		try:
			d[option] = config.get('cortez',option)
		except:
			print('Exception on {}'.format(option))
			d[option] = None
	return d