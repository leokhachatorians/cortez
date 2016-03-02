import sys
from colorama import init
from config import Config
from our_parser import parser
import concurrent.futures
import soundcloud
from cortez_downloader import CortezDownloader

if __name__ == '__main__':
	init(autoreset=True)
	args = parser.parse_args()
	config = Config()
	client = soundcloud.Client(client_id=config.CLIENT_ID)
	downloader = CortezDownloader(client, config)
	if args.choice == 'download':
		if len(args.urls) == 0:
			print('Need a track or playlist URL in order to download.')
			sys.exit(1)
		with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
		    for url in args.urls:
		        executor.submit(downloader.download, url)
	elif args.choice == 'login':
		if args.direct:
			print('Direct flow')
		else:
			downloader.test_auth()
	elif args.choice == 'config':
		config.open_config()
	if len(sys.argv) == 1:
		parser.print_help()