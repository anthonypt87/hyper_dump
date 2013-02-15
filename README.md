# hyper_dump
hyper_dump is a small module for downloading songs from [Hype Machine](http://www.hypem.com).

## Requirements
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)  
[Requests](http://docs.python-requests.org/en/latest/)

## Usage

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
													Number of pages of songs to download. If unset,
													downloads all songs
		-v, --verbose         Verbose mode

## Example
	python hypeer_dump.py -u anthonypt87 -o ~anthony/mp3s -m 2 -v
This will download the first two pages of user anthonypt87's songs to ~anthony/mp3s in verbose mode.

	python hyper_dump.py -u hyperdump -o ~anthony/mp3s
This will download all of user hyperdump's songs to ~anthony/mp3s.
