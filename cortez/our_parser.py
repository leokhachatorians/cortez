import argparse

class Parser(argparse.ArgumentParser):
    def error(self, error):
            sys.stderr.write("\nError: {}\n".format(error))
            self.print_help()
            sys.exit(2)

parser = Parser(description="cortez, a SoundCloud downloader.")

parser.add_argument(
	'-d','--download',
	help="""
	Downloads given tracks via URL, space delimited. Quality is capped at 128kbps .mp3 as per
	Soundcloud API""",
	nargs="*")

parser.add_argument(
    '-l', '--login',
    help="Login to access your liked tracks and other features",
    type=str)

parser.add_argument(
	'-pl', '--playlist',
	help="Download a given playlist via URL",
	type=str)