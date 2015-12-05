#!/usr/bin/env python2

import os
import requests
import sys

from tumblr_auth import consumer_key, consumer_secret, oauth_token, oauth_secret

sys.path.append("pytumblr")
import pytumblr


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
    user = sys.argv[1]
    pictures = []

    # Authenticate via OAuth
    client = pytumblr.TumblrRestClient(
                consumer_key,
                consumer_secret,
                oauth_token,
                oauth_secret)

    posts_info = client.posts(user)
    for post in posts_info.get('posts'):
        data = post.get('photos')
        if not data:
            continue
        data = data[0]
        print data['original_size']['url']
        pictures.append(data['original_size']['url'])

    if not os.path.exists(user):
        os.mkdir(user)

    download_dir = os.path.join(os.getcwd(), user)
    for url in pictures:
        #print requests.get(url, stream=True)
        print download_file(url, download_dir), "downloaded!"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: tumblr_pic_getter.py [TUMBLR_USER]"
        sys.exit(0)
    main()
