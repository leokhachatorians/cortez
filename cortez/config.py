import configparser
import sys

class ConfigSetup(object):
	def __init__(self):
		self.path = 'config.cfg'
		self.setup_config()

	def setup_config(self):
		try:
			config = configparser.ConfigParser()
			config.read(self.path)
			self.CLIENT_ID = config.get('app_settings', 'client_id')
			self.CLIENT_SECRET = config.get('app_settings', 'client_secret')
			self.REDIRECT_URI = config.get('app_settings', 'redirect_uri')
			self.SAVE_PATH = config.get('general', 'where_to_save')
			self.SAVE_TOKEN = config.getboolean('oauth', 'save_token')
		except Exception as e:
			print(e)
			print('Improper configuration, please check your config.cfg file')
			sys.exit(1)