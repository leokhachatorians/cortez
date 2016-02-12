from oauth import OAuthHelper
import urllib
from colorama import Fore, Back

class CortezDownloader(object):
	def __init__(self, client, config):
		self.client = client
		self.config = config

	def track_info_api_call(self, track_id):
		track_info = self.client.get('/tracks/{0}'.format(track_id))
		return track_info

	def get_stream_url(self, track):
		stream_url = self.client.get(track.stream_url, allow_redirects=False)
		return stream_url

	def save_track_to_disk(self, url, title):
		urllib.request.urlretrieve(url, title+'.mp3')

	def format_track_name(self, track):
		remove = '#/\\\'\"'
		track_name = track.user['username'] + ' - ' + track.title
		track_name = track_name.translate((str.maketrans("","",), remove))
		return track_name

	def resolve_url(self, url):
		info = self.client.get('/resolve', url=url)
		return info

	def stream_download_workflow(self, track):
		stream_url = self.get_stream_url(track)
		title = self.format_track_name(track)
		self.color_print('Starting download of ', title)
		self.save_track_to_disk(stream_url.location, title)

	def direct_download_workflow(self, track):
		url = track.download_url + '?client_id=' + self.config.CLIENT_ID
		title = self.format_track_name(track)
		self.color_print('Starting download of ', title)
		self.save_track_to_disk(url, title)

	def check_download_argument(self, url):
	    try:
	        resolved = self.resolve_url(url)
	        return resolved
	    except:
	        print("Error: URL given seems to be invalid")
	        sys.exit(1)

	def check_if_downloadable(self, track):
		if track.downloadable:
			return True

	def download_a_track(self, track_id):
		try:
			track = self.track_info_api_call(track_id)
			if track.downloadable:
				self.direct_download_workflow(track)
			else:
				self.stream_download_workflow(track)
			print("....saved")
		except Exception as e:
			print('Caught an exception: {}'.format(e))

	def download_a_playlist(self, playlist_info):
		for track in playlist_info.tracks:
			self.download_a_track(track['id'])
		print('Finished downloading entire playlist.')

	def check_if_track_or_playlist(self, url):
		info = self.check_download_argument(url)
		try:
			if info.track_count:
				return ['playlist', info]
		except Exception as e:
			print(e)
			return ['track', info]

	def color_print(self, message, data,end=False):
		if end:
			end='\n'
		else:
			end=''
		print(message + Fore.GREEN + Back.BLACK + data, end=end)

	def test_auth(self):
		check = OAuthHelper(self.config)
		if check.oauth_flow():
			user = check.user
			print('Succesfully authenticated.')
			self.color_print('Welcome, ',user.get('/me').username, end=True)
			return user
		else:
			print('Authentication failed.')
			sys.exit(1)