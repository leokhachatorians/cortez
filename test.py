import soundcloud
import urllib
import argparse

CLIENT_ID = "a1a76b5205bb80d8f7ad182133028016"
client = soundcloud.Client(client_id=CLIENT_ID)
parser = argparse.ArgumentParser(description="Sonic, a simple SoundCloud downloader.")
parser.add_argument(
	'-d','--download',
	help="Downloads Given Tracks",
	nargs="*")

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
			# print(track_info, track_info.title, track_info.id)
			stream_url = get_stream_url(client, stream_info)
			# print(stream_url.location)
			track_name = format_track_name(track_info.title)
			download_track(stream_url.location, track_name)
			print('Succesfully downloaded {}'.format(track_name))
		except Exception as e:
			print('Caught an exception: {}'.format(e))


if __name__ == '__main__':
	args = parser.parse_args()
	if args.download:
		download_tracks_workflow(args.download)
	else:
		print('You need to pass a url to download!')

# track_info = get_track_info_via_url(client, url)
# try:
# 	name = format_track_name(track_info.title)
# except:
# 	track_info = get_track_info_via_id(client, track_info.id)

# print(name)
# s_url = get_stream_url(client, track_info.id)
# download_track(s_url.location)