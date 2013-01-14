import argparse
import logging
import os
import user_song_downloader

DEFAULT_USERNAME = 'popular'
DEFAULT_OUTPUT_DIRECTORY = 'mp3s'
DEFAULT_PAGES_TO_DOWNLOAD = 1

def get_args():
	parser = argparse.ArgumentParser(description="Download hype machine songs")
	parser.add_argument(
		'-u',
		'--username', 
		help='Username of the user to download songs from (default=%s)' % DEFAULT_USERNAME,
		default=DEFAULT_USERNAME
	)
	parser.add_argument(
		'-o',
		'--output-directory', 
		help='Username of the user to download songs from (default=%s)' % DEFAULT_OUTPUT_DIRECTORY,
		default='mp3s'
	)
	parser.add_argument(
		'-m',
		'--max-pages', 
		help='Number of pages of songs to download (default=%s)' % DEFAULT_PAGES_TO_DOWNLOAD, 
		type=int, 
		default=DEFAULT_PAGES_TO_DOWNLOAD
	)
	parser.add_argument(
		'-v', 
		'--verbose', 
		help='Verbose mode',
		action='store_true', 
	)

	return parser.parse_args()

if __name__ == '__main__':
	args = get_args()

	if not os.path.exists(args.output_directory):
		os.mkdir(args.output_directory)

	if args.verbose:
		logger = user_song_downloader.logger
		logger.setLevel(logging.INFO)
		logger.info('Verbose mode enabled')

	downloader = user_song_downloader.UserSongDownloader(args.output_directory)
	downloader.download_from_user(username=args.username, max_pages=args.max_pages)

