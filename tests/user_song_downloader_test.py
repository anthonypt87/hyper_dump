import mock
import os
import shutil
import tempfile
import unittest

import user_song_downloader


class UserSongDownloaderIntegrationTest(unittest.TestCase):

	def setUp(self):
		self.temp_dir = tempfile.mkdtemp()
		assert os.path.exists(self.temp_dir)

	def tearDown(self):
		shutil.rmtree(self.temp_dir)
		assert not os.path.exists(self.temp_dir)

	def test_user_song_downloader_downloads_one_thing(self):
		downloader = user_song_downloader.UserSongDownloader(self.temp_dir)
		downloader.download_from_user(
			username='hyperdump',
			max_pages=1
		)
		assert os.listdir(self.temp_dir)


class UserSongDownloaderUnitTest(unittest.TestCase):

	def setUp(self):
		self.mock_page = mock.Mock()
		self.mock_get_page_patcher = mock.patch(
			'user_song_downloader.Page.get_page',
			return_value=self.mock_page
		)
		self.mock_get_page = self.mock_get_page_patcher.start()
		self.mock_download_songs_from_page_patcher = mock.patch(
			'user_song_downloader.SongDownloader.download_songs_from_page'
		)
		self.mock_download_songs_from_page = self.mock_download_songs_from_page_patcher.start()

	def tearDown(self):
		self.mock_get_page_patcher.stop()
		self.mock_download_songs_from_page_patcher.stop()

	def test_download_from_user(self):
		downloader = user_song_downloader.UserSongDownloader('mock_directory')
		downloader.download_from_user(
			username='hyperdump',
			max_pages=1
		)
		self.mock_get_page.assert_called_once_with(
			'hyperdump',
			1
		)
		self.mock_download_songs_from_page.assert_called_once_with(
			self.mock_page
		)

	def test_download_from_user_stops_early_if_pages_dont_exist(self):
		downloader = user_song_downloader.UserSongDownloader('mock_directory')
		self.mock_get_page.side_effect = [self.mock_page, None]

		downloader.download_from_user(
			username='hyperdump',
			max_pages=3000
		)
		self.mock_get_page.assert_any_call(
			'hyperdump',
			1
		)
		self.mock_get_page.assert_any_call(
			'hyperdump',
			2
		)
		assert self.mock_get_page.call_count == 2

		self.mock_download_songs_from_page.assert_called_once_with(
			self.mock_page
		)

	def test_downloads_all_if_max_pages_is_none(self):
		downloader = user_song_downloader.UserSongDownloader('mock_directory')
		self.mock_get_page.side_effect = [self.mock_page, self.mock_page, None]
		downloader.download_from_user(
			username='hyperdump',
			max_pages=None
		)

		assert self.mock_get_page.call_count == 3
		for page in range(1,4):
			self.mock_get_page.assert_any_call(
				'hyperdump',
				page
			)

		assert self.mock_download_songs_from_page.call_count == 2


class SongDownloaderTest(unittest.TestCase):

	def setUp(self):
		self.mock_file = mock.MagicMock()
		self.mock_open_patcher = mock.patch(
			'__builtin__.open',
			return_value=self.mock_file
		)
		self.mock_open = self.mock_open_patcher.start()
		self.mock_open.return_value.__enter__ = lambda s: s

		self.song = mock.Mock(
			artist='I',
			title='Download Songs',
			id='some_id',
			key='some_key',
			cookies='cookies'
		)
		self.page = mock.Mock(
				songs=[self.song]
		)

	def tearDown(self):
		self.mock_open_patcher.stop()

	def test_download_songs_from_page(self):
		song_downloader = user_song_downloader.SongDownloader('directory')
		with mock.patch('user_song_downloader.requests.get', return_value=mock.Mock(content='data')) as mock_get:
			song_downloader.download_songs_from_page(self.page)
			mock_get.assert_called_with(
				'http://hypem.com/serve/play/some_id/some_key.mp3',
				cookies=self.song.cookies
			)

			self.mock_open.assert_called_with(
				'directory/I - Download Songs.mp3',
				'w'
			)
			self.mock_file.write.assert_called_with(
				'data'
			)

	def test_doesnt_download_song_if_song_already_exists(self):
		song_downloader = user_song_downloader.SongDownloader('directory')
		with mock.patch('user_song_downloader.os.path.exists', return_value=True) as mock_exists:
			song_downloader.download_songs_from_page(self.page)
			mock_exists.assert_called_once_with('directory/I - Download Songs.mp3')
			assert not self.mock_open.called

	def test_slashes_are_removed_from_output_file_name(self):
		self.song.artist = '/////I'
		self.song.title = 'Download/ ///Songs'
		song_downloader = user_song_downloader.SongDownloader('directory')
		with mock.patch('user_song_downloader.requests.get', return_value=mock.Mock(content='data')) as mock_get:
			song_downloader.download_songs_from_page(self.page)
			mock_get.assert_called_with(
				'http://hypem.com/serve/play/some_id/some_key.mp3',
				cookies=self.song.cookies
			)

			self.mock_open.assert_called_with(
				'directory/I - Download Songs.mp3',
				'w'
			)
			self.mock_file.write.assert_called_with(
				'data'
			)


class PageTest(unittest.TestCase):

	def get_mock_data(self):
		with open('tests/datafiles/sample_user_page.html') as mock_data_file:
			return mock_data_file.read()

	def test_get_page(self):
		mock_cookies = mock.Mock()
		with mock.patch(
			'user_song_downloader.requests.get', 
			return_value=mock.Mock(
				text=self.get_mock_data(),
				cookies=mock_cookies
			)
		) as mock_get:
			page = user_song_downloader.Page.get_page(
				'hyperdump',
				1
			)
			mock_get.assert_called_with(
				'http://hypem.com/hyperdump/1',
				params={
					'ax': 1
				}
			)

		assert len(page.songs) == 1
		song = page.songs[0]
		assert song == user_song_downloader.Song(
			'Ellie Goulding',
			'Lights (Shook Remix)',
			'19t8s',
			'9309d1b3bbcd89c137449a4c21f6288e',
			cookies=mock_cookies
		)
