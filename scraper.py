# Copyright Anshuman73.
# Visit anshuman73.github.io for more info.
# Released under MIT License.
# Works with Python 2.7

import json
import urllib
import os
from optparse import OptionParser
import datetime
import sys

verbose = False
logging = False

def log(string):
    global verbose
    global logging
    if verbose:
        print string
    if logging:
        with open("log", "a") as log_file:
            date_time = datetime.datetime.now().strftime('%d/%m/%y - %H:%m:%S')
            log_file.write('{}: {}\n'.format(date_time, string))

def download_image(number, directory, prefix=""):
    url = 'http://xkcd.com/{}/info.0.json'.format(number)
    img_metadata = json.loads(urllib.urlopen(url).read())
    image_file = '{}{}-{}'.format(prefix, number, img_metadata['safe_title'])
    file_path = '{}/{}'.format(directory, image_file)
    if not os.path.exists(file_path):
        log('Downloading image: ' + image_file)
        urllib.urlretrieve(img_metadata['img'], file_path)
    else:
        log('Image' + image_file + '" already exists. Skipping...')

def update_status_indicator(current, total):
    global verbose
    bar_length = 70
    if not verbose:
        bar = '[='
        progress = int(float(current) / float(total) * float(bar_length))
        bar += '=' * progress
        bar += ' ' * (bar_length - progress)
        bar += '] {}/{}'.format(current, total)
        if total == current:
            bar += '\n'
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

def download_all(directory, prefix=""):
    log('Querying Total Number of Images as of now...')
    total = json.loads(urllib.urlopen('http://xkcd.com/info.0.json').read())['num']
    log('Querying complete\n\nTotal of ' + str(total) + ' images found\n\n')
    log('Checking if /images directory exists...\n')
    if not os.path.exists(directory):
        log('Making directory {}'.format(directory))
        os.makedirs(directory)
    for num in xrange(1, total + 1):
        if num == 404:
            log('\n\nImage 404 is a pathetic little joke -__- Ignoring...\n\n')
            continue
        download_image(num, directory, prefix=prefix)
        update_status_indicator(num, total)

def parse_args():
    parser = OptionParser(usage="usage: python scraper.py [options]")
    parser.add_option(
        "-a", "--autostart",
        action = "store_true",
        default = False
    )
    parser.add_option(
        "-v", "--verbose",
        action = "store_true",
        default = False
    )
    parser.add_option(
        "-l", "--log",
        action = "store_true",
        default = False
    )
    parser.add_option(
        "-d", "--directory",
        action = "store",
        default = os.getcwd() + '/images'
    )
    parser.add_option(
        "-p", "--prefix",
        action = "store",
        default = ""
    )
    return parser.parse_args()

def main():
    (options, args) = parse_args()

    global verbose
    global logging
    verbose = options.verbose
    logging = options.log

    #Cleaning directory input - Removing / at the end if it was entered
    if options.directory[-1] == '/':
        options.directory = options.directory[0:-1]

    if options.autostart or raw_input('\nPress Enter to start:') == '':
        download_all(options.directory, prefix = options.prefix)

main()
