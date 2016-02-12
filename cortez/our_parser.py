import argparse
import textwrap
import sys

class Parser(argparse.ArgumentParser):
    def error(self, error):
            print("\nError: {}".format(error))
            self.print_help()
            sys.exit(1)

parser = Parser(
	prog='cortez',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=textwrap.dedent('''\
	-----------------------------------
	| cortez, a SoundCloud downloader |
	-----------------------------------
		- download tracks and entire playlists.
		- login into your SoundCloud account and have
			  full control within your terminal.
	'''))

### Downloading Parser ###
sub_parser = parser.add_subparsers(
	dest="choice")

sub_download = sub_parser.add_parser(
	'download', 
	help='\
	Downloads given tracks or playlists via URL. Quality is capped at 128kbps .mp3 as per\
	Soundcloud API unless otherwise noted')

sub_download.add_argument(
	'urls',
	nargs="*")

### Login Parser ###
sub_login = sub_parser.add_parser(
	'login',
	help='Login into SoundCloud')

sub_login.add_argument(
	'login',
	action="store_true")

sub_login.add_argument('-d','--direct',
	action="store_true")

### Config Parser ###
sub_config = sub_parser.add_parser(
	'config',
	help="Manage and edit cortez to your liking")

sub_config.add_argument(
	'config',
	action="store_true")