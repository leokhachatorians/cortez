from flask import Flask, request
import requests
import config
import soundcloud
import webbrowser
import os
import time
import logging
import sys

class OAuthHelper(object):
	def __init__(self, client_id, app):
		self.client_id = client_id
		self.app = app
		self.user = None
		self.token = None

	def check_if_token_exists(self):
		if os.path.isfile('.access_token'):
			return True
		else:
			return False

	def authenticate(self):
		auth_url = soundcloud.Client(
			client_id=self.client_id,
			redirect_uri=config.REDIRECT_URI)
		webbrowser.open(auth_url.authorize_url())
		time.sleep(1.5)

	def check_token(self, token):
		try:
			self.user = soundcloud.Client(access_token=token)
			self.user.get('/me').username
			return True
		except:
			return False

	def oauth_flow(self):
		if not self.check_if_token_exists():
			print('No token was found.')
			print('Will open a browser window to authenticate.')
			self.authenticate()
			self.token = input('Access Token: ')
			if self.check_token(self.token):
				if config.SAVE_TOKEN:
					self.write_token(self.token)
			else:
				print('Invalid Token')
				return False
		else:
			self.token = self.read_token()

		print('Checking access token...',end='')

		# if self.check_token(self.token):
		# 	return True
		# else:
		# 	return False
		return self.check_token(self.token)

	def write_token(self, token):
		with open('.access_token','w') as f:
			f.write(token)

	def read_token(self):
		with open('.access_token','r') as t:
				token = t.read()
		return token

############################
#  Local Server for OAuth  #
############################
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
@app.route('/')
def index():
	return ''

@app.route('/grab')
def grab():
	code = request.args.get('code')
	url = "https://api.soundcloud.com/oauth2/token"
	payload = {
	'client_id':config.CLIENT_ID,
	'client_secret':config.CLIENT_SECRET,
	'grant_type':'authorization_code',
	'redirect_uri':config.REDIRECT_URI,
	'code':code
	}
	try:
		r = requests.post(url, data=payload)
		if r.raise_for_status() is None:
			data = r.json()
			if data['access_token']:
				write_token(data['access_token'])
		else:
			return 'Failed to retrieve'
		return 'Succesfully authenticated, you may close this window.'
	except Exception as e:
		print(e)
		return 'You didn\'t authorize ;_;'
	finally:
		shutdown_server()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()