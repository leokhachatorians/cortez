import soundcloud
import urllib
import argparse
import sys


class Parser(argparse.ArgumentParser):
        def error(self, error):
                sys.stderr.write("\nError: {}\n".format(error))
                self.print_help()
                sys.exit(2)


CLIENT_ID = "a1a76b5205bb80d8f7ad182133028016"
client = soundcloud.Client(client_id=CLIENT_ID)
parser = Parser(description="Sonic, a simple SoundCloud downloader.")
parser.add_argument(
	'-d','--download',
	help="Downloads given tracks via URL, space delimited",
	nargs="*")

parser.add_argument(
        '-l', '--login',
        help="Login to access your liked tracks and other features",
        type=str)

url = "http://soundcloud.com/deepmixnation/best-vocal-deep-uk-house-music-113-by-xypo"

def get_track_info_via_url(client, url):
	track_info = client.get('/resolve', url=url)
	return track_info

def fetch_track_to_stream(client, track_id):
	track_info = client.get('/tracks/{0}'.format(track_id))
	return track_info

def get_stream_url(client, stream_info):
	stream_url = client.get(stream_info.stream_url, allow_redirects=False)
	return stream_url

def download_track(stream_url, name):
	urllib.request.urlretrieve(stream_url, name+'.mp3')

def format_track_name(track_name):
	track_name = track_name.replace(' ','_').replace('#','')
	return track_name

def download_tracks_workflow(urls):
	for url in urls:
		try:
			track_info = get_track_info_via_url(client, url)
			stream_info = fetch_track_to_stream(client, track_info.id)
			stream_url = get_stream_url(client, stream_info)
			track_name = format_track_name(track_info.title)
			print('Starting downlaod of {}'.format(track_name))
			download_track(stream_url.location, track_name)
			print('Succesfully downloaded {}'.format(track_name))
		except Exception as e:
			print('Caught an exception: {}'.format(e))

def get_play_list(url):
        try:
                a = client.get('/resolve', url=url)
                print(a)
                return a
        except Exception as e:
                print(e)


a = get_play_list("https://soundcloud.com/eemilybowmann/sets/mine")
for i in a.tracks:
        print(i['id'])
        stream_info = fetch_track_to_stream(client, i['id'])
        stream_url = get_stream_url(client, stream_info)
        track_name = format_track_name(i['title'])
        print(track_name)
        download_track(stream_url.location, track_name)
        
"""
if __name__ == '__main__':
	args = parser.parse_args()
	if args.download:
		download_tracks_workflow(args.download)
	else:
		parser.print_help()
"""

# track_info = get_track_info_via_url(client, url)
# try:
# 	name = format_track_name(track_info.title)
# except:
# 	track_info = get_track_info_via_id(client, track_info.id)

# print(name)
# s_url = get_stream_url(client, track_info.id)
# download_track(s_url.location)
