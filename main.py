import time
import datetime
from google_searching_script import Query
from auxiliary_functions import determine_ssl


def main():

    determine_ssl()
    print("Google Searching Script\n")


if __name__ == '__main__':
    start_time = time.time()
    print("Starting new task:")
    main()
    time = time.time() - start_time
    print("Task executed in "+str(datetime.timedelta(seconds=time)))
