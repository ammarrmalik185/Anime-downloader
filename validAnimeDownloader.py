from Downloader import Downloader
import os
import selenium

sep = "<EP>"
valid_anime_list = []
downloaded_animes = []
downloaded_animes_ep = []
run_1 = [False]

exceptionControl = [0, 10]


def downloaded_anime_check():
    if os.path.isfile(r"cache(beta)\recently downloaded animes.txt"):
        file = open(r"cache(beta)\recently downloaded animes.txt", "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            parts = line.split(sep)
            downloaded_animes.append(parts[0].lower())
            downloaded_animes_ep.append(parts[1].lower())
    else:
        open(r"cache(beta)\recently downloaded animes.txt", "w")
        run_1[0] = True


def valid_anime_check():
    if os.path.isfile(r"cache(beta)\valid animes.txt"):
        file = open(r"cache(beta)\valid animes.txt", "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            if line != "" and line != " ":
                valid_anime_list.append(line.lower())
    else:
        open(r"cache(beta)\valid animes.txt", "w")
        run_1[0] = True


def save(downloaded_anime_name, ep):
    text = ""
    count = 0
    while True:
        try:
            text += str(downloaded_anime_name[count]+sep+ep[count]) + "\n"
            count += 1
        except IndexError:
            file = open(r"cache(beta)\recently downloaded animes.txt", "w", encoding='utf-8')
            file.write(text)
            file.close()
            break


def core():

    crawler = Downloader(valid_anime_list, downloaded_animes, downloaded_animes_ep, True)

    crawler.force_res = 720

    crawler.get_links(crawler.get_main_page())

    crawler.filter()

    crawler.link_set_maker()

    info = crawler.return_values()

    print("-------------------------Found but not downloading--------------------------\n")

    titles_to_print = []

    for i in info[0]:
        single_anime_string = ""
        single_anime_string += ("Name       :" + info[0][i][0]) + "\n"
        single_anime_string += ("Episode no :" + info[0][i][1]) + "\n"
        single_anime_string += ("Release    :" + info[0][i][3]) + "\n"
        titles_to_print.append(single_anime_string)

    count = len(titles_to_print) - 1
    current = count
    while current >= 0:
        print(titles_to_print[current])
        current -= 1

    if len(info[2]) != 0:
        print("---------------------------------Downloading--------------------------------\n")

        for i in info[2]:
            print("Name       :" + info[2][i][0])
            print("Episode no :" + info[2][i][1])
            print("Release    :" + info[2][i][3])
            print("")

    if len(info[2]) != 0:
        crawler.download_link_append()

        info = crawler.return_values()
        if len(info[3]) != 0:
            print('Errors :')
            for i in info[3]:
                print(i)

        done, done_eps = crawler.download_all()
        anime_no = len(done)
        for i in info[0]:
            done.append(info[0][i][0])
            done_eps.append(info[0][i][1])

        save(done, done_eps)

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
        input("the program has generated the required files.\n")
    else:
        try:
            core()
        except selenium.common.exceptions.SessionNotCreatedException:
            input("session creation failed")
        except Exception:
            exceptionControl[0] += 1
            if exceptionControl[0] < exceptionControl[1]:
                print("Error occurred .. retrying")
                run_main()
            else:
                input("max exceptions occurred .. press enter to exit...")


run_main()
