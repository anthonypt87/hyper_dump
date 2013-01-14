hyper_dump
==========

Hype machine downloader

usage: hyper_dump.py [-h] [-u USERNAME] [-o OUTPUT_DIRECTORY] [-m MAX_PAGES]
                     [-v]

Download hype machine songs

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username of the user to download songs from
                        (default=popular)
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Username of the user to download songs from
                        (default=mp3s)
  -m MAX_PAGES, --max-pages MAX_PAGES
                        Number of pages of songs to download (default=1)
  -v, --verbose         Verbose mode


Sample:
python -u anthonypt87 -o ~anthony/mp3s -m 2 -v
This will download the first two pages of anthonypt87's songs to ~anthony/mp3s in verbose mode.
