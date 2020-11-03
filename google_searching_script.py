# Google Searching Script (GSS) for automated search for given queries
import time
import sys
import webbrowser
import urllib.error
import http.client as httplib
from termcolor import colored
from googlesearch import search
from googletrans import Translator
from auxiliary_functions import *


class Query:
    def __init__(self, keyword, how_many, pause):
        self.keyword = keyword
        self.how_many = how_many
        self.pause = pause
        if pause < 2:
            self.pause = 2
        self.translator = Translator()

    def search(self, language, domain):
        # start_time = time.time()
        # check if files are present, if not create them
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
        # filtering
        for x in range(len(existing_websites)):
            existing_websites[x] = extract_keyword(existing_websites[x])
        filtered_list = []
        # script loop working condition
        condition = True
        # expected amount of results
        desired_results = self.how_many
        # check internet connection
        try:
            httplib.HTTPConnection("www.google.com", timeout=5).request("HEAD", "/")
        except:
            print(colored("Connection error", "red"))
            return False
        # keyword
        keyword = self.translator.translate(self.keyword, dest=language)
        print('Searching "' + str(keyword.text) + '" on google.' + domain + ' in "' + language + '" with ' + str(
            self.pause) + ' lapse pause time:')
        # searching loop
        while condition:
            # break loop if desired amount of results is fulfilled
            if len(filtered_list) == desired_results:
                condition = False
            # check internet connection
            try:
                httplib.HTTPConnection("www.google.com", timeout=10).request("HEAD", "/")
            except:
                print(colored("Connection error", "red"))
                return False
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
                                # append website to temporary list
                                filtered_list.append(filtered_website)
                                website = website[0:].split('/')
                                website = website[0] + "//" + website[2]
                                # return found website
                                save_to_file = open("data/existing_websites.txt", "a+")
                                save_to_file.write(website+"\n")
                                save_to_file.close()
                                print("\t"+str(website))
                                # open URL
                                webbrowser.open(website, new=0, autoraise=True)
                            else:
                                self.how_many += 1
                                print("\t"+colored(str(filtered_website), "magenta"))
                        else:
                            self.how_many += 1
                            print("\t"+colored(str(filtered_website), "magenta"))
                    else:
                        self.how_many += 1
                        print("\t"+colored(str(filtered_website), "magenta"))
                    # break loop if desired amount of results is fulfilled
                    if len(filtered_list) == desired_results:
                        break
                    time.sleep(0.5)
            except urllib.error.HTTPError:
                print(colored("\n\tError 429: ", "red") + "Too many requests")
                print("\tRestoring connection in:")
                for i in range(120, 0, -1):
                    sys.stdout.write("\t" + str(i))
                    sys.stdout.flush()
                    time.sleep(1)
                print()
        print("Found " + str(len(filtered_list)) + " results on " + str(self.how_many) + " inquiries")
        self.how_many = desired_results
        # print("Executed in %s seconds\n" % (time.time() - start_time))
