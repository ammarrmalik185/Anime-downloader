import os

modules_a = True
try:
    import selenium
except ModuleNotFoundError:
    input("You have not installed python module: \"selenium\", please install "
          "it by using \"pip install selenium\" in command prompt")
    modules_a = False

try:
    import idm
except ModuleNotFoundError:
    input("You have not installed python module: \"idm\", please install "
          "it by using \"pip install idm\" in command prompt")
    modules_a = False

if not modules_a:
    input("Since the program does not have the required files, it will exit")
    exit()

from Core import *
from selenium.common.exceptions import *

options = Options(
    confirmation=False,
    # weather or not you need to press OK to add each file to idm or not
    silent=True,
    # will the program do all activities in background or not
    alternate_quality=True,
    # if the program does not find the anime in the required resolution, it will download in best resolution possible
    logs=False,
    # the program will create logs (used for debugging)
    download_path="C:\\Animes",
    # your download path
    pages_to_scan=1,
    # how many pages should the program scan for animes
    quality={"type": "force_res", "value": "1080p"},
    # in what resolution should the episodes be downloaded (360p, 480p, 720p, 1080p, or source),
    auto_exit=False,
    # should the program automatically handle errors?
    auto_exception_control=True,
    # automatically handle exceptions
    max_refresh_page=5,
    # if the crawler fails to open a page, how many times should it retry?
    generate_log_file=False
    # program will create a core.log file to log events
)

sep = "<EP>"
valid_anime_list = []
downloaded_animes = []
downloaded_animes_ep = []
run_1 = [False]

exceptionControl = [0, 10]


def downloaded_anime_check():
    if os.path.isfile(r"cache\recently downloaded animes.txt"):
        file = open(r"cache\recently downloaded animes.txt", "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            parts = line.split(sep)
            downloaded_animes.append(parts[0].lower())
            downloaded_animes_ep.append(parts[1].lower())
    else:
        if not os.path.exists(r"cache"):
            os.makedirs(r"cache")
        open(r"cache\recently downloaded animes.txt", "w")
        run_1[0] = True


def valid_anime_check():
    if os.path.isfile(r"cache\valid animes.txt"):
        file = open(r"cache\valid animes.txt", "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            if line != "" and line != " ":
                valid_anime_list.append(line.lower())
    else:
        if not os.path.exists(r"cache"):
            os.makedirs(r"cache")
        open(r"cache\valid animes.txt", "w")
        run_1[0] = True


def save(downloaded_anime_name, ep):
    text = ""
    count = 0
    while True:
        try:
            text += str(downloaded_anime_name[count] + sep + ep[count]) + "\n"
            count += 1
        except IndexError:
            file = open(r"cache\recently downloaded animes.txt", "w", encoding='utf-8')
            file.write(text)
            file.close()
            break


def core():

    crawler = Crawler([valid_anime_list, downloaded_animes, downloaded_animes_ep], options)

    crawler.start_part_1()
    info = crawler.get_mid_term_data()

    if len(info[1]) != 0:
        print("-------------------------Found but not downloading--------------------------\n")

        print_strings = []
        for i in info[1]:
            single_anime_string = ""
            single_anime_string += ("Name       : " + i["name"]) + "\n"
            single_anime_string += ("Episode no : " + i["ep_no"]) + "\n"
            print_strings.append(single_anime_string)

        print_strings.reverse()
        for i in print_strings:
            print(i)

    if len(info[0]) != 0:
        print("---------------------------------Downloading--------------------------------\n")

        print_strings = []
        for i in info[0]:
            single_anime_string = ""
            single_anime_string += ("Name       : " + i["name"]) + "\n"
            single_anime_string += ("Episode no : " + i["ep_no"]) + "\n"
            print_strings.append(single_anime_string)

        print_strings.reverse()
        for i in print_strings:
            print(i)

    crawler.start_part_2()

    anime_no = 0
    end_data = crawler.get_end_term_data()
    for data in end_data[0]:
        if data["status"] == "200":
            anime_no += 1

    for data in end_data[1]:
        if data["status"] == "504":
            print(data["name"] + " Episode No : " + data["ep_no"] + " unable to load")
        if data["status"] == "404":
            print(data["name"] + " Episode No : " + data["ep_no"] + " not found in selected quality")

    save_data = crawler.get_save_data()
    save(save_data[0], save_data[1])

    crawler.download_animes()
    crawler.close_crawler()

    if options.auto_exit:
        exit()

    if anime_no != 0:
        re = input(str(anime_no) + " anime(s) downloading ...press enter to continue")
    else:
        re = input("No animes to download ...press enter to continue")

    if re == "rerun":
        valid_anime_list.clear()
        downloaded_animes.clear()
        downloaded_animes_ep.clear()
        valid_anime_check()
        downloaded_anime_check()
        run_1[0] = False
        core()


def run_main():
    valid_anime_list.clear()
    downloaded_animes.clear()
    downloaded_animes_ep.clear()
    run_1[0] = False

    valid_anime_check()
    downloaded_anime_check()
    if run_1[0]:
        print("the program has generated the required files.\n")
    else:
        try:
            core()
        except SessionNotCreatedException:
            input("Session creation failed, make sure that chromedriver.exe is in the folder and "
                  "is updated to your chrome browser version")
        except Exception as ex:
            print(str(ex.args))
            if not options.auto_exception_control:
                raise ex
            exceptionControl[0] += 1
            if exceptionControl[0] < exceptionControl[1]:
                print("major error occurred .. retrying")
                run_main()
            else:
                input("major error occurred too many times, cannot continue .. press enter to exit...")


run_main()
