import configparser

def get_option(category):
	d = {}

	config = configparser.ConfigParser()
	config.read('config.cfg')

	options = config.options(category)

	for option in options:
		try:
			d[option] = config.get(category,option)
		except:
			print('Exception on {}'.format(option))
			d[option] = None
	return d

config = configparser.ConfigParser()
config.read('config.cfg')


CLIENT_ID = config.get('app_settings', 'client_id')
CLIENT_SECRET = config.get('app_settings', 'client_secret')
REDIRECT_URI = config.get('app_settings', 'redirect_uri')
SAVE_PATH = config.get('general', 'where_to_save')
SAVE_TOKEN = config.getboolean('oauth', 'save_token')