import shutil
import os
import tempfile
import unittest
import hyper_dump

class HyperDumpIntegrationTest(unittest.TestCase):

	def setUp(self):
		self.temp_dir = tempfile.mkdtemp()
		assert os.path.exists(self.temp_dir)

	def tearDown(self):
		shutil.rmtree(self.temp_dir)
		assert not os.path.exists(self.temp_dir)

	def test_hyper_dump_downloads_one_thing(self):
		pass


