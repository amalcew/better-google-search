# auxiliary functions for scripts
__author__ = "Aleksander Malcew"
__version__ = "1.0.2"
__maintainer__ = "Aleksander Malcew"
__email__ = "amalcew@tutanota.com"

import ssl
import os


def convert_to_list(file):
    try:
        file = open(file, encoding='utf-8').readlines()
    except FileNotFoundError:
        file = open(file, "w+").readlines()
    if not "\n" in file[-1]:
        file[-1] = file[-1] + "\n"
    file = [w[:-1] for w in file]
    return file


def extract_keyword(url):
    url = str(url)
    if url.find('https') != -1:
        if url.find('www') != -1:
            url = url[12:].split('/')
            url = url[0]
            url = url.split('.')
            keyword = url[0]
        else:
            url = url[8:].split('/')
            url = url[0]
            url = url.split('.')
            if len(url[0]) != 2:
                keyword = url[0]
            else:
                keyword = url[1]
    elif url.find('http') != -1:
        if url.find('www') != -1:
            url = url[11:].split('/')
            url = url[0]
            url = url.split('.')
            keyword = url[0]
        else:
            url = url[7:].split('/')
            url = url[0]
            url = url.split('.')
            keyword = url[0]
    elif url.find('www') != -1:
        url = url[4:].split('.')
        keyword = url[0]
    else:
        url = url[0:].split('.')
        keyword = url[0]
    return keyword


def determine_ssl():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
