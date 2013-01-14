import json
import logging
import os
import requests

from BeautifulSoup import BeautifulSoup
from collections import namedtuple


def get_logger():
	logging_format = '%(message)s'
	logging.basicConfig(level=logging.ERROR, format=logging_format)
	return logging.getLogger('hyper_dump')


logger = get_logger()


class UserSongDownloader(object):
	
	def __init__(self, output_directory):
		self._output_directory = output_directory

	def download_from_user(self, username, max_pages):
		"""Downloads songs to `self._output_directory` for a particular username
		Args:
			username -- username of user to download songs from
			max_pages -- int denoting number of pages to download. If None, downloads all songs
		"""
		logger.info('Downloading songs to directory: %s' % self._output_directory)
		song_downloader = SongDownloader(self._output_directory)

		current_page_number = 1
		while current_page_number <= max_pages or max_pages is None:
			logger.info('Working on page %s' % (current_page_number))

			page = Page.get_page(username, current_page_number)
			if page is None:
				logger.info(
					"Page %s doesn't exist. %s was probably the last page. We're finished!" % (current_page_number, current_page_number - 1)
				)
				break

			song_downloader.download_songs_from_page(page)
			current_page_number += 1


class SongDownloader(object):

	def __init__(self, output_directory):
		self._output_directory = output_directory

	def download_songs_from_page(self, page):
		for song in page.songs:
			logger.info('Downloading song %s - %s' % (song.artist, song.title))

			song_filename = self._get_song_filename(song)
			song_path = os.path.join(self._output_directory, song_filename) 

			if os.path.exists(song_path):
				logger.info('%s already exists' % song_path)
				continue

			song_data = requests.get(
				'http://hypem.com/serve/play/{id}/{key}.mp3'.format(id=song.id, key=song.key),
				cookies=song.cookies
			)

			with open(song_path, 'w') as song_file:
				song_file.write(song_data.content)

	def _get_song_filename(self, song):
		def normalize_string(string):
			return string.replace('/', '')
		normalized_artist_name = normalize_string(song.artist)
		normalized_title = normalize_string(song.title)
		return u'{artist} - {title}.mp3'.format(artist=normalized_artist_name, title=normalized_title)

class Page(object):
	def __init__(self, songs):
		self.songs = songs

	@classmethod
	def get_page(cls, username, page_number):
		page_request = requests.get(
				'http://hypem.com/{username}/{page_number}'.format(username=username, page_number=page_number),
				params={
					# By default, hypem pages load the songs via some AJAX.
					# ax=1 renders the page in a minimal way, loading the 
					# song information in advance
					'ax': 1
				}
		)
		soup = BeautifulSoup(page_request.text)
		display_list = soup.find(id='displayList-data')
		if display_list is None:
			return
		song_infos = json.loads(display_list.text)['tracks']

		songs = []
		for song_info in song_infos:
			songs.append(
				Song(
					artist=song_info['artist'],
					title=song_info['song'],
					id=song_info['id'],
					key=song_info['key'],
					cookies=page_request.cookies
				)
			)

		return cls(songs)


# A little weird cookie info is here...
Song = namedtuple('Song', ['artist', 'title', 'id', 'key', 'cookies'])
