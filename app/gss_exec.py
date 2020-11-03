__author__ = "Aleksander Malcew"
__version__ = "1.0.2"
__maintainer__ = "Aleksander Malcew"
__email__ = "amalcew@tutanota.com"

import time
import datetime
import urllib3.exceptions
from requests import exceptions
from socket import gaierror
from google_searching_script import Query
from auxiliary_functions import determine_ssl


languages = ['aa', 'ab', 'af', 'am', 'ar', 'as', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bn', 'bo', 'br', 'ca',
             'co', 'cs', 'cy', 'da', 'de', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fj', 'fo', 'fr',
             'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'ha', 'hi', 'he', 'hr', 'hu', 'hy', 'ia', 'id', 'ie', 'ik', 'in',
             'is', 'it', 'iu', 'iw', 'ja', 'ji', 'jw', 'ka', 'kk', 'kl', 'km', 'kn', 'ko', 'ks', 'ku', 'ky', 'la',
             'ln', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'na', 'ne', 'nl',
             'no', 'oc', 'om', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sd', 'sg',
             'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg',
             'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'vo', 'wo',
             'xh', 'yi', 'yo', 'za', 'zh', 'zu']

domains = ['ae', 'am', 'as', 'at', 'az', 'ba', 'be', 'bg', 'bi', 'bs', 'ca', 'cd', 'cg', 'ch', 'ci', 'cl', 'co.bw',
           'co.ck', 'co.cr', 'co.hu', 'co.id', 'co.il', 'co.im', 'co.in', 'co.je', 'co.jp', 'co.ke', 'co.kr',
           'co.ls', 'co.ma', 'co.nz', 'co.th', 'co.ug', 'co.uk', 'co.uz', 'co.ve', 'co.vi', 'co.za', 'co.zm', 'com',
           'com.af', 'com.ag', 'com.ar', 'com.au', 'com.bd', 'com.bo', 'com.br', 'com.bz', 'com.co', 'com.cu',
           'com.do', 'com.ec', 'com.eg', 'com.et', 'com.fj', 'com.gi', 'com.gt', 'com.hk', 'com.jm', 'com.kw',
           'com.ly', 'com.mt', 'com.mx', 'com.my', 'com.na', 'com.nf', 'com.ni', 'com.np', 'com.om', 'com.pa',
           'com.pe', 'com.ph', 'com.pk', 'com.pr', 'com.py', 'com.qa', 'com.sa', 'com.sb', 'com.sg', 'com.sv',
           'com.tj', 'com.tr', 'com.tw', 'com.ua', 'com.uy', 'com.uz', 'com.vc', 'com.vn', 'cz', 'de', 'dj', 'dk',
           'dm', 'ee', 'es', 'fi', 'fm', 'fr', 'gg', 'gl', 'gm', 'gr', 'hn', 'hr', 'ht', 'hu', 'ie', 'is', 'it',
           'jo', 'kg', 'kz', 'li', 'lk', 'lt', 'lu', 'lv', 'md', 'mn', 'ms', 'mu', 'mw', 'net', 'nl', 'no', 'nr',
           'nu', 'off.ai', 'org', 'pl', 'pn', 'pt', 'ro', 'ru', 'rw', 'sc', 'se', 'sh', 'si', 'sk', 'sm', 'sn',
           'tm', 'to', 'tp', 'tt', 'tv', 'uz', 'vg', 'vu', 'ws', 'com']

help_languages = ['-- A --', 'aa - Afar', 'ab - Abkhazian', 'af - Afrikaans', 'am - Amharic', 'ar - Arabic',
                  'as - Assamese', 'ay - Aymara', 'az - Azerbaijani', '', '-- B --', 'ba - Bashkir',
                  'be - Byelorussian', 'bg - Bulgarian', 'bh - Bihari', 'bi - Bislama', 'bn - Bengali; - Bangla',
                  'bo - Tibetan', 'br - Breton', '', '-- C --', 'ca - Catalan', 'co - Corsican', 'cs - Czech',
                  'cy - Welsh', '', '-- D --', 'da - Danish', 'de - German', 'dz - Bhutani', '', '-- E --',
                  'el - Greek', 'en - English', 'eo - Esperanto', 'es - Spanish', 'et - Estonian', 'eu - Basque',
                  '', '-- F --', 'fa - Persian', 'fi - Finnish', 'fj - Fiji', 'fo - Faeroese', 'fr - French',
                  'fy - Frisian', '', '-- G --', 'ga - Irish', 'gd - Scots - Gaelic', 'gl - Galician',
                  'gn - Guarani', 'gu - Gujarati', '', '-- H --', 'ha - Hausa', 'hi - Hindi', 'hr - Croatian',
                  'hu - Hungarian', 'hy - Armenian', '', '-- I --', 'ia - Interlingua', 'ie - Interlingue',
                  'ik - Inupiak', 'in - Indonesian', 'is - Icelandic', 'it - Italian', 'iw - Hebrew', '', '-- J --',
                  'ja - Japanese', 'ji - Yiddish', 'jw - Javanese', '', '-- K --', 'ka - Georgian', 'kk - Kazakh',
                  'kl - Greenlandic', 'km - Cambodian', 'kn - Kannada', 'ko - Korean', 'ks - Kashmiri',
                  'ku - Kurdish', 'ky - Kirghiz', '', '-- L --', 'la - Latin', 'ln - Lingala', 'lo - Laothian',
                  'lt - Lithuanian', 'lv - Latvian, - Lettish', '', '-- M --', 'mg - Malagasy', 'mi - Maori',
                  'mk - Macedonian', 'ml - Malayalam', 'mn - Mongolian', 'mo - Moldavian', 'mr - Marathi',
                  'ms - Malay', 'mt - Maltese', 'my - Burmese', '', '-- N --', 'na - Nauru', 'ne - Nepali',
                  'nl - Dutch', 'no - Norwegian', '', '-- O --', 'oc - Occitan', 'om - (Afan) - Oromo',
                  'or - Oriya', '', '-- P --', 'pa - Punjabi', 'pl - Polish', 'ps - Pashto, - Pushto',
                  'pt - Portuguese', '', '-- Q --', 'qu - Quechua', '', '-- R --', 'rm - Rhaeto-Romance',
                  'rn - Kirundi', 'ro - Romanian', 'ru - Russian', 'rw - Kinyarwanda', '', '-- S --',
                  'sa - Sanskrit', 'sd - Sindhi', 'sg - Sangro', 'sh - Serbo-Croatian', 'si - Singhalese',
                  'sk - Slovak', 'sl - Slovenian', 'sm - Samoan', 'sn - Shona', 'so - Somali', 'sq - Albanian',
                  'sr - Serbian', 'ss - Siswati', 'st - Sesotho', 'su - Sundanese', 'sv - Swedish', 'sw - Swahili',
                  '', '-- T --', 'ta - Tamil', 'te - Tegulu', 'tg - Tajik', 'th - Thai', 'ti - Tigrinya',
                  'tk - Turkmen', 'tl - Tagalog', 'tn - Setswana', 'to - Tonga', 'tr - Turkish', 'ts - Tsonga',
                  'tt - Tatar', 'tw - Twi', '', '-- U --', 'uk - Ukrainian', 'ur - Urdu', 'uz - Uzbek', '',
                  '-- V --', 'vi - Vietnamese', 'vo - Volapuk', '', '-- W --', 'wo - Wolof', '', '-- X --',
                  'xh - Xhosa', '', '-- Y --', 'yo - Yoruba', '', '-- Z --', 'zh - Chinese', 'zu - Zulu']

help_domains = ['google.ae', 'google.am', 'google.as', 'google.at', 'google.az', 'google.ba', 'google.be',
                'google.bg', 'google.bi', 'google.bs', 'google.ca', 'google.cd', 'google.cg', 'google.ch',
                'google.ci', 'google.cl', 'google.co.bw', 'google.co.ck', 'google.co.cr', 'google.co.hu',
                'google.co.id', 'google.co.il', 'google.co.im', 'google.co.in', 'google.co.je', 'google.co.jp',
                'google.co.ke', 'google.co.kr', 'google.co.ls', 'google.co.ma', 'google.co.nz', 'google.co.th',
                'google.co.ug', 'google.co.uk', 'google.co.uz', 'google.co.ve', 'google.co.vi', 'google.co.za',
                'google.co.zm', 'google.com', 'google.com.af', 'google.com.ag', 'google.com.ar', 'google.com.au',
                'google.com.bd', 'google.com.bo', 'google.com.br', 'google.com.bz', 'google.com.co',
                'google.com.cu', 'google.com.do', 'google.com.ec', 'google.com.eg', 'google.com.et',
                'google.com.fj', 'google.com.gi', 'google.com.gt', 'google.com.hk', 'google.com.jm',
                'google.com.kw', 'google.com.ly', 'google.com.mt', 'google.com.mx', 'google.com.my',
                'google.com.na', 'google.com.nf', 'google.com.ni', 'google.com.np', 'google.com.om',
                'google.com.pa', 'google.com.pe', 'google.com.ph', 'google.com.pk', 'google.com.pr',
                'google.com.py', 'google.com.qa', 'google.com.sa', 'google.com.sb', 'google.com.sg',
                'google.com.sv', 'google.com.tj', 'google.com.tr', 'google.com.tw', 'google.com.ua',
                'google.com.uy', 'google.com.uz', 'google.com.vc', 'google.com.vn', 'google.cz', 'google.de',
                'google.dj', 'google.dk', 'google.dm', 'google.ee', 'google.es', 'google.fi', 'google.fm',
                'google.fr', 'google.gg', 'google.gl', 'google.gm', 'google.gr', 'google.hn', 'google.hr',
                'google.ht', 'google.hu', 'google.ie', 'google.is', 'google.it', 'google.jo', 'google.kg',
                'google.kz', 'google.li', 'google.lk', 'google.lt', 'google.lu', 'google.lv', 'google.md',
                'google.mn', 'google.ms', 'google.mu', 'google.mw', 'google.net', 'google.nl', 'google.no',
                'google.nr', 'google.nu', 'google.off.ai', 'google.org', 'google.pl', 'google.pn', 'google.pt',
                'google.ro', 'google.ru', 'google.rw', 'google.sc', 'google.se', 'google.sh', 'google.si',
                'google.sk', 'google.sm', 'google.sn', 'google.tm', 'google.to', 'google.tp', 'google.tt',
                'google.tv', 'google.uz', 'google.vg', 'google.vu', 'google.ws', 'gooogle.com']


def main():
    determine_ssl()
    print("Google Searching Script v1.0.2, made by Aleksander Malcew\n")
    print("Skrypt automatycznie wyszukuje podane hasło, otwierając wyszukane linki w domyślnej przeglądarce "
          "internetowej")
    print("Wyszukując hasło, pamiętaj, że proces obciąża serwery Google które przy zbyt wysokiej ilości zapytań na "
          "sekundę mogą zablokować twoje IP (błąd 429)")
    print("Dla najskuteczniejszych wyników, szukaj haseł w ich rodzimym języku (np. Ford po angielsku)\n")
    while True:
        print("Aby zakończyć działanie skryptu, wpisz słowo 'exit'")
        print("Aby rozpocząć wyszukiwanie, wpisz słowo 'search'")
        print("Aby zobaczyć listę dostepnych języków, wpisz słowo 'lang'")
        print("Aby zobaczyć listę dostepnych domen Google, wpisz słowo 'google'")
        mode = input()
        if mode == 'exit':
            break
        elif mode == 'lang':
            print("\nDostępne języki wyszukiwania i tłumaczenia: ")
            for x in range(len(help_languages)):
                print(help_languages[x])
        elif mode == 'google':
            print("\nDostępne domeny google: ")
            for x in range(len(help_domains)):
                print(help_domains[x])
        elif mode == 'search':
            while True:
                word = input("Wpisz szukane hasło: ")
                if word == '' or word.isspace():
                    print("Niepoprawne hasło. Spróbuj ponownie")
                else:
                    break
            while True:
                how_many = input("Wpisz pożądaną ilość wyników (aby uniknąć błędu 429, najlepiej poniżej 40): ")
                try:
                    how_many = int(how_many)
                    break
                except ValueError:
                    print("Niepoprawna ilość. Spróbuj ponownie")
            while True:
                language = input("Podaj język wyszukiwania (wg. standardu ISO 639-2, np. 'en', 'ru', 'es' etc.): ")
                if not language in languages:
                    print("Niepoprawny język. Spróbuj ponownie")
                else:
                    break
            while True:
                domain = input("Podaj domenę google (bez pierwszej kropki, np. 'com', 'ru', 'com.py'): ")
                if not domain in domains:
                    print("Niepoprawna domena. Spróbuj ponownie")
                else:
                    break
            start_time = time.time()
            Query(word, how_many, 10).search(language, domain)
            t = time.time() - start_time
            print("Wyszukiwanie trwało " + str(datetime.timedelta(seconds=t)))
        else:
            print("Niepoprawny tryb. Spróbuj ponownie")


if __name__ == '__main__':
    main()
