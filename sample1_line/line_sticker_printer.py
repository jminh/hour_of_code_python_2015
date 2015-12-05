#!/usr/bin/env python2

from bs4 import BeautifulSoup as BS
import os
import requests
import sys


def download_file(url, dir='.'):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(os.path.join(dir, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def main():
    stickers = []
    res = requests.get(sys.argv[1])
    soup = BS(res.text, 'html.parser')

    for tag in soup.find_all('span'):
        if u'style' not in tag.attrs:
            continue
        style = tag['style']
        l_parentheses = style.rfind('(') + 1
        r_parentheses = style.rfind(')')
        path = style[l_parentheses:r_parentheses]
        print path
        stickers.append(path)

    title = soup.title.text.split('-')[0].strip()
    if not os.path.exists(title):
        os.mkdir(title)

    download_dir = os.path.join(os.getcwd(), title)
    for url in stickers:
        print download_file(url, download_dir), "downloaded!"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: line_sticker_printer.py [URL]"
        sys.exit(0)
    main()
