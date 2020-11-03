# Google Searching Script (GSS) for automated search for given queries
__author__ = "Aleksander Malcew"
__version__ = "1.0.2"
__maintainer__ = "Aleksander Malcew"
__email__ = "amalcew@tutanota.com"

import time
import os
import webbrowser
import sys
import urllib.error
import http.client as httplib
from googlesearch import search
from googletrans import Translator
from auxiliary_functions import convert_to_list, extract_keyword


class Query:
    def __init__(self, keyword, how_many, pause):
        self.keyword = keyword
        self.how_many = how_many
        self.pause = pause
        if pause < 2:
            self.pause = 2
        self.translator = Translator()

    def search(self, language, domain):
        # filtering
        try:
            os.mkdir("./data")
        except FileExistsError:
            pass
        try:
            banned_keywords = convert_to_list("data/banned_keywords.txt")
        except IndexError:
            banned_keywords = []
        try:
            existing_websites = convert_to_list("data/existing_websites.txt")
            # check for newlines in existing_websites
            check = open("data/existing_websites.txt", "r+", encoding='utf-8')
            check_lines = check.readlines()
            check.close()
            if not any('\n' in x for x in check_lines[-1]):
                check = open("data/existing_websites.txt", "a")
                check.write("\n")
                check.close()
        except IndexError:
            existing_websites = []
        for x in range(len(existing_websites)):
            existing_websites[x] = extract_keyword(existing_websites[x])
        filtered_list = []
        # script loop working condition
        condition = True
        # expected amount of results
        desired_results = self.how_many
        # check connection
        while True:
            try:
                httplib.HTTPConnection("www.google.com", timeout=10).request("HEAD", "/")
                break
            except:
                print("\nBrak połączenia internetowego")
                print("Ponawianie próby nawiązania połączenia")
                for i in range(10, 0, -1):
                    sys.stdout.write(str(i) + " - ")
                    sys.stdout.flush()
                    time.sleep(1)
                print()
        # keyword
        keyword = self.translator.translate(self.keyword, dest=language)
        wait_x = 0
        wait = ["x    x....", ".x    x...", "..x    x..", "...x    x.", "....x    x",
                "...x    x.", "..x    x..", ".x    x..."]
        print('\nWyszukiwanie "' + str(keyword.text) + '" na google.' + domain + ' w języku "' + language + '": ')
        # searching loop
        while condition:
            # break loop if desired amount of results is fulfilled
            if len(filtered_list) == desired_results:
                condition = False
            # check connection
            while True:
                try:
                    httplib.HTTPConnection("www.google.com", timeout=10).request("HEAD", "/")
                    break
                except:
                    print("\nBrak połączenia internetowego")
                    print("Ponawianie próby nawiązania połączenia")
                    for i in range(10, 0, -1):
                        sys.stdout.write(str(i) + " - ")
                        sys.stdout.flush()
                        time.sleep(1)
                    print()
            # google search
            try:
                for website in search(keyword.text, tld=domain, lang=language, num=self.how_many, stop=self.how_many,
                                      pause=self.pause):
                    # convert website url to website keyword
                    filtered_website = extract_keyword(website)
                    # filtering
                    if not any(filtered_website in x for x in banned_keywords):
                        if not any(filtered_website in y for y in existing_websites):
                            if not any(filtered_website in z for z in filtered_list):
                                wait_x = 0
                                # append website to temporary list
                                filtered_list.append(filtered_website)
                                website = website[0:].split('/')
                                website = website[0] + "//" + website[2]
                                # return found website
                                save_to_file = open("data/existing_websites.txt", "a+")
                                save_to_file.write(website+"\n")
                                save_to_file.close()
                                print(str(website))
                                # open URL
                                webbrowser.open(website, new=0, autoraise=True)
                            else:
                                self.how_many += 1
                                print(wait[wait_x])
                                wait_x += 1
                                if wait_x == 8:
                                    wait_x = 0
                        else:
                            self.how_many += 1
                            print(wait[wait_x])
                            wait_x += 1
                            if wait_x == 8:
                                wait_x = 0
                    else:
                        self.how_many += 1
                        print(wait[wait_x])
                        wait_x += 1
                        if wait_x == 8:
                            wait_x = 0
                    # break loop if desired amount of results is fulfilled
                    if len(filtered_list) == desired_results:
                        break
                    time.sleep(1)
            except urllib.error.HTTPError:
                print("\nBłąd 429: Zbyt wiele zapytań")
                print("Ponawianie próby nawiązania połączenia")
                for i in range(10, 0, -1):
                    sys.stdout.write(str(i) + " - ")
                    sys.stdout.flush()
                    time.sleep(1)
                print()
        print("Znaleziono " + str(len(filtered_list)) + " wyników na " + str(self.how_many) + " wykonanych zapytań")
        self.how_many = desired_results
