import urllib
import sys
from colorama import Fore, Back, init
from config import client, CLIENT_ID
from our_parser import parser

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

def get_play_list(client, url):
        try:
                playlist = resolve_url(client, url)
                return playlist
        except Exception as e:
                print("Error: {}".format(e))
                sys.exit(2)

def check_if_downloadable(track):
	if track.downloadable:
		return True

def download_a_track(urls):
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
	playlist = get_play_list(client, url)
	for track in playlist.tracks:
		track = track_info_api_call(client, track['id'])
		stream_url = get_stream_url(client, track)
		track_name = format_track_name(track.title)
		color_print('Starting download of ',track_name)
		save_track_to_disk(stream_url.location, track_name)
		print("....saved")
	print('Finished downloading entire playlist.')

def color_print(message, track_name):
	print(message + Fore.GREEN + Back.BLACK + track_name, end="")

if __name__ == '__main__':
	init(autoreset=True)
	args = parser.parse_args()
	if args.download:
		download_a_track(args.download)
	elif args.playlist:
		download_a_playlist(args.playlist)
	else:
		parser.print_help()