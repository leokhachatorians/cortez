import sys
from colorama import init
from config import ConfigSetup
from our_parser import parser
import soundcloud
from cortez_downloader import CortezDownloader

if __name__ == '__main__':
	init(autoreset=True)
	args = parser.parse_args()
	config = ConfigSetup()
	client = soundcloud.Client(client_id=config.CLIENT_ID)
	downloader = CortezDownloader(client, config)
	if args.choice == 'download':

		if len(args.urls) == 0:
			print('Need a track or playlist URL in order to download.')
			sys.exit(1)

		for url in args.urls:
			check = downloader.check_if_track_or_playlist(url)
			if check[0] == 'playlist':
				downloader.download_a_playlist(check[1])
			elif check[0] == 'track':
				downloader.download_a_track(check[1].id)

	elif args.choice == 'login':
		if args.direct:
			print('Direct flow')
		else:
			downloader.test_auth()
	elif args.choice == 'config':
		print('configure flow')

	if len(sys.argv) == 1:
		parser.print_help()