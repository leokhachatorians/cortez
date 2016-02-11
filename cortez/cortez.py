import urllib
import sys
from colorama import Fore, Back, init
from config import CLIENT_ID, get_option
from our_parser import parser
import requests
import soundcloud
from oauth import app, OAuthHelper

def track_info_api_call(client, track_id):
	track_info = client.get('/tracks/{0}'.format(track_id))
	return track_info

def get_stream_url(client, track):
	stream_url = client.get(track.stream_url, allow_redirects=False)
	return stream_url

def save_track_to_disk(url, title):
	urllib.request.urlretrieve(url, title+'.mp3')

def format_track_name(track):
	remove = '#/\\\'\"'
	track_name = track.user['username'] + ' - ' + track.title
	track_name = track_name.translate((str.maketrans("","",), remove))
	return track_name

def resolve_url(client, url):
	info = client.get('/resolve', url=url)
	return info

def stream_download_workflow(client, track):
	stream_url = get_stream_url(client, track)
	title = format_track_name(track)
	color_print('Starting download of ', title)
	save_track_to_disk(stream_url.location, title)

def direct_download_workflow(client, track):
	url = track.download_url + '?client_id=' + CLIENT_ID
	title = format_track_name(track)
	color_print('Starting download of ', title)
	save_track_to_disk(url, title)

def check_download_argument(client, url):
    try:
        resolved = resolve_url(client, url)
        return resolved
    except:
        print("Error: URL given seems to be invalid")
        sys.exit(2)

def check_if_downloadable(track):
	if track.downloadable:
		return True

def download_a_track(client, track_id):
	try:
		track = track_info_api_call(client, track_id)
		if track.downloadable:
			direct_download_workflow(client, track)
		else:
			stream_download_workflow(client, track)
		print("....saved")
	except Exception as e:
		print('Caught an exception: {}'.format(e))

def download_a_playlist(client, playlist_info):
	for track in playlist_info.tracks:
		download_a_track(client, track['id'])
	print('Finished downloading entire playlist.')

def check_if_track_or_playlist(client, url):
	info = check_download_argument(client, url)
	try:
		if info.track_count:
			return ['playlist', info]
	except Exception as e:
		print(e)
		return ['track', info]

def color_print(message, data,end=False):
	if end:
		end='\n'
	else:
		end=''
	print(message + Fore.GREEN + Back.BLACK + data, end=end)

def test_auth():
	check = OAuthHelper(CLIENT_ID, app)
	if check.oauth_flow():
		user = check.user
		print('Succesfully authenticated.')
		color_print('Welcome, ',user.get('/me').username, end=True)
		return user
	else:
		print('Authentication failed.')
		sys.exit(2)

if __name__ == '__main__':
	init(autoreset=True)
	args = parser.parse_args()
	if args.choice == 'download':
		if len(args.urls) == 0:
			print('Need a track or playlist URL in order to download.')
			sys.exit(2)
		client = soundcloud.Client(client_id=CLIENT_ID)
		for url in args.urls:
			check = check_if_track_or_playlist(client, url)
			if check[0] == 'playlist':
				download_a_playlist(client, check[1])
			elif check[0] == 'track':
				download_a_track(client, check[1].id)
	elif args.choice == 'login':
		if args.direct:
			print('Direct flow')
		else:
			test_auth()
	elif args.choice == 'config':
		print('configure flow')

	if len(sys.argv) == 1:
		parser.print_help()