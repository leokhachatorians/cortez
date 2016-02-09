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
        except Exception as e:
                print("Error: {}".format(e))
                sys.exit(2)

def check_if_downloadable(track):
	if track.downloadable:
		return True

def download_a_track(urls):
	client = soundcloud.Client(client_id=CLIENT_ID)
	urls = check_download_argument(client, urls)
	for url in urls:
		try:
			track_info = resolve_url(client, url)
			track = track_info_api_call(client, track_info.id)
			if not check_if_downloadable(track):
				stream_download_workflow(client, track)
			else:
				direct_download_workflow(client, track)
			print("....saved")
		except Exception as e:
			print('Caught an exception: {}'.format(e))

def download_a_playlist(url):
	client = soundcloud.Client(client_id=CLIENT_ID)
	playlist = check_download_argument(client, url)
	for track in playlist.tracks:
		track = track_info_api_call(client, track['id'])
		stream_url = get_stream_url(client, track)
		track_name = format_track_name(track.title)
		color_print('Starting download of ',track_name)
		save_track_to_disk(stream_url.location, track_name)
		color_print('Saved ', track_name)
	print('Finished downloading entire playlist.')

def color_print(message, data):
	print(message + Fore.GREEN + Back.BLACK + data + '.')

def test_auth():
	check = OAuthHelper(CLIENT_ID, app)
	if check.oauth_flow():
		user = check.user
		print('Succesfully authenticated.')
		color_print('Welcome, ',user.get('/me').username)
	else:
		print('Authentication failed.')
		sys.exit(2)

# def get_user_info():
# 	with open('.access_token','r') as t:
# 		token = t.read()
# 	user = soundcloud.Client(access_token=token)
# 	print(user.get('/me').username)
# init(autoreset=True)
# test_auth()
# get_user_info()

	# print(client.authorize_url())
	# print('running')
	# time.sleep(1)
	# webbrowser.open(client.authorize_url())

	# print(helper.shutdown_server())
	# print(client.authorize_url())

# def test_config():
# 	d = {}
# 	config = configparser.ConfigParser()
# 	config.read('config.cfg')
# 	option = config.options('cortez')
# 	if config.get('cortez', 'colors'):
# 		print('colorrr')
# 	else:
# 		print('no')
	# print(config.sections())



# client = soundcloud.Client(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     username='leokhachatorians@gmail.com',
#     password='leoisub3r'
# 	)

# 	print(client.get('/me').username)

# test_auth()

# print(get_option()['save_token'])
# print(get_option()['colors'])
# print(get_option()['save_folder'])
if __name__ == '__main__':
	init(autoreset=True)
	args = parser.parse_args()
	try:
		if args.urls:
			print(args.urls)
		else:
			print('Need a track or playlist URL in order to download.')
	except:
		pass

	try:
		if args.login:
			if args.direct:
				print('Username n password plz')
			print('logging in')
	except:
		pass

	if len(sys.argv) == 1:
		parser.print_help()
	# if args.urls:
	# 	print(args.urls)
	# else:
	# 	print('Need a track or playlist URL in order to download.')

	# 	test_auth()
	# elif args.direct_login:
	# 	print('Coming soon')
	# else:
	# 	parser.print_help()