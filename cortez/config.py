import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

CLIENT_ID = config.get('app_settings', 'client_id')
CLIENT_SECRET = config.get('app_settings', 'client_secret')
REDIRECT_URI = config.get('app_settings', 'redirect_uri')
SAVE_PATH = config.get('general', 'where_to_save')
SAVE_TOKEN = config.getboolean('oauth', 'save_token')