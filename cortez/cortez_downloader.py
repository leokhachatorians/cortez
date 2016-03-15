from oauth import OAuthHelper
import urllib
from colorama import Fore, Back
import sys

class CortezDownloader(object):
	def __init__(self, client, config):
		self.client = client
		self.config = config

	def download(self, url):
		check = self.check_if_track_or_playlist(url)
		if check[0] == 'playlist':
			self.download_a_playlist(check[1])
		elif check[0] == 'track':
			self.download_a_track(check[1].id)

	def track_info_api_call(self, track_id):
		track_info = self.client.get('/tracks/{0}'.format(track_id))
		return track_info

	def get_stream_url(self, track):
		try:
			stream_url = self.client.get(track.stream_url, allow_redirects=False)
			return stream_url
		except AttributeError:
			print(Fore.RED + Back.WHITE + 'ERROR: That song is unable to be downloaded.')
			sys.exit(1)

	def save_track_to_disk(self, url, title):
		urllib.request.urlretrieve(url, self.config.SAVE_PATH + title + '.mp3')

	def format_track_name(self, track):
		remove = '#/\\\'\"'
		track_name = track.user['username'] + ' - ' + track.title
		track_name = track_name.translate((str.maketrans("","",), remove))
		return track_name

	def resolve_url(self, url):
		info = self.client.get('/resolve', url=url)
		return info

	def stream_download_workflow(self, track, title):
		stream_url = self.get_stream_url(track)
		self.save_track_to_disk(stream_url.location, title)

	def direct_download_workflow(self, track, title):
		url = track.download_url + '?client_id=' + self.config.CLIENT_ID
		self.save_track_to_disk(url, title)

	def check_download_argument(self, url):
	    try:
	        resolved = self.resolve_url(url)
	        return resolved
	    except:
	        print("Error: Seems to be an issue fetching that track; may be private.")
	        sys.exit(1)

	def check_if_downloadable(self, track):
		if track.downloadable:
			return True

	def download_a_track(self, track_id):
		track = self.track_info_api_call(track_id)
		title = self.format_track_name(track)
		self.color_print('Downloading ',title)
		if track.downloadable:
			self.direct_download_workflow(track, title)
		else:
			self.stream_download_workflow(track, title)
		self.color_print('Finished downloading ', title)

	def download_a_playlist(self, playlist_info):
		for track in playlist_info.tracks:
			self.download_a_track(track['id'])
		print('Finished downloading entire playlist.')

	def check_if_track_or_playlist(self, url):
		info = self.check_download_argument(url)
		try:
			if info.track_count:
				return ['playlist', info]
		except:
			return ['track', info]

	def color_print(self, message, data):
		print(message + Back.BLUE + Fore.WHITE + data)

	def test_auth(self):
		check = OAuthHelper(self.config)
		if check.oauth_flow():
			user = check.user
			print('Succesfully authenticated.')
			self.color_print('Welcome, ',user.get('/me').username)
			return user
		else:
			print('Authentication failed.')
			sys.exit(1)
