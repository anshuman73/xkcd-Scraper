# Copyright Anshuman73.
# Visit anshuman73.github.io for more info.
# Released under MIT License.
# Works with Python 2.7

import json
import urllib
import os
from optparse import OptionParser

def download_all(directory):
    print 'Querying Total Number of Images as of now...'
    total = json.loads(urllib.urlopen('http://xkcd.com/info.0.json').read())['num']
    print 'Querying complete\n\nTotal of ' + str(total) + ' images found\n\n'
    base_url = 'http://xkcd.com/%s/info.0.json'
    print 'Checking if /images directory exists...\n'
    if not os.path.exists(directory):
        print 'Making directory {}'.format(directory)
        os.makedirs(directory)
    for num in xrange(1, total + 1):
        if num == 404:
            print '\n\nImage 404 is a pathetic little joke -__- Ignoring...\n\n'
            continue

        url = base_url % (num)
        img_metadata = json.loads(urllib.urlopen(url).read())
        image_file = '{}-{}'.format(num, img_metadata['safe_title'])
        file_path = '{}/{}'.format(directory, image_file)
        if not os.path.exists(file_path):
            print 'Downloading image: ' + image_file
            urllib.urlretrieve(img_metadata['img'], file_path)
        else:
            print 'Image' + image_file + '" already exists. Skipping...'

def main():
    parser = OptionParser(usage="usage: python scraper.py [options]")
    parser.add_option(
        "-a", "--autostart",
        action = "store_true",
        default = False
    )
    parser.add_option(
        "-d", "--directory",
        action = "store",
        default = os.getcwd() + '/images'
    )
    (options, args) = parser.parse_args()

    #Cleaning directory input - Removing / at the end if it was entered
    if options.directory[-1] == '/':
        options.directory = options.directory[0:-1]

    if options.autostart or raw_input('\nPress Enter to start:') == '':
        download_all(options.directory)


main()
