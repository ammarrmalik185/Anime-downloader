from bs4 import BeautifulSoup
from selenium import webdriver
import os
import webbrowser
import time



def downloaded_anime_check():
    if os.path.isfile("recently downloaded animes.txt"):
        file = open("recently downloaded animes.txt","r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            downloaded_animes.append(line)
    else:
        open("recently downloaded animes.txt","w")


def valid_anime_check():
    if os.path.isfile("valid animes.txt"):
        file = open("valid animes.txt","r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            valid_anime_list.append(line)
    else:
        open("valid animes.txt","w")

def get_html_text_main_page():
    driver = webdriver.Chrome()
    url = "https://horriblesubs.info/"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def main_urls_getter(code):
    links = []
    names = code.findAll("a", {})
    for i in names:
        link = i.get('href')
        link = str(link)
        links.append(link)
    return links


def parse_list_use_full(links, url):
    use_full_links = []
    check = 1
    for no in range(1, len(links)-1):
        if links[no] == "#":
                if check == 1:
                    check = 0
                elif check == 0:
                    break

        if check == 0:
            links[no] = url + links[no]
            use_full_links.append(links[no])
    use_full_links = use_full_links[1:len(use_full_links)]
    return use_full_links


def link_source_code_getter(url_list):
    source_codes = []
    driver = webdriver.Chrome()
    for url in url_list:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        source_codes.append(soup)
    driver.quit()
    return source_codes


def source_code_info_getter(source_code):
    title = source_code.findAll("h1", {"class": "entry-title"})
    title = title[0].get_text()
    # release_dates = source_code.findAll("span", {"class": "rls-date"})
    magnet_links = source_code.findAll("a", {"title": "Magnet Link"})
    torrent_links = source_code.findAll("a", {"title": "Torrent Link"})
    episode_nos = source_code.findAll("div", {"class": "rls-info-container"})
    episode_no_list = []
    for element in episode_nos:
        episode_no = element.get("id")
        episode_no_list.append(episode_no)
    text = ""
    text = text + str(title) + "\n----------------------------------------------\n"
    try:
        start_1 = 0
        start_2 = 0
        start_3 = 0
        if len(magnet_links) == 39:
            text += "Batch (" + episode_no_list[0] + "):\n"
            text += "480p:\n\tMagnet link : " + str(magnet_links[0].get('href')) + "\n"
            text += "720p:\n\tMagnet link : " + str(magnet_links[1].get('href')) + "\n"
            text += "1080p:\n\tMagnet link : " + str(magnet_links[2].get('href')) + "\n"
            start_1 += 1
            start_2 += 3
        text += "480p:" + "\n"
        for _ in range(len(episode_no_list) - start_1):
            text += "Episode no " + str(episode_no_list[start_1]) + ":\n"
            text += "\tMagnet link : " + str(magnet_links[start_2].get('href')) + "\n"
            text += "\tTorrent link : " + str(torrent_links[start_3].get('href')) + "\n"
            start_1 += 1
            start_2 += 3
            start_3 += 3

        start_1 = 0
        start_2 = 1
        start_3 = 1
        if len(magnet_links) == 39:
            start_1 += 1
            start_2 += 3

        text += "720p:" + "\n"
        for _ in range(len(episode_no_list) - start_1):
            text += "Episode no " + str(episode_no_list[start_1]) + ":\n"
            text += "\tMagnet link : " + str(magnet_links[start_2].get('href')) + "\n"
            text += "\tTorrent link : " + str(torrent_links[start_3].get('href')) + "\n"
            start_1 += 1
            start_2 += 3
            start_3 += 3

        start_1 = 0
        start_2 = 2
        start_3 = 2
        if len(magnet_links) == 39:
            start_1 += 1
            start_2 += 3
        text += "1080p:" + "\n"
        for _ in range(len(episode_no_list) - start_1):
            text += "Episode no " + str(episode_no_list[start_1]) + ":\n"
            text += "\tMagnet link : " + str(magnet_links[start_2].get('href')) + "\n"
            text += "\tTorrent link : " + str(torrent_links[start_3].get('href')) + "\n"
            start_1 += 1
            start_2 += 3
            start_3 += 3
    except IndexError:
        pass
    return text, title, magnet_links


def create_and_save():
    download_count = 0
    if not os.path.exists("Animes\\"):
        os.makedirs("Animes\\")
    source_code_main = get_html_text_main_page()
    complete_links = main_urls_getter(source_code_main)
    use_full_links = parse_list_use_full(complete_links, "https://horriblesubs.info")
    source_codes_list = link_source_code_getter(use_full_links)

    downloaded_anime_name = []
    c =  "1" #choice_getter()
    for code in source_codes_list:
        text, title, link_list = source_code_info_getter(code)
        try:
            file = open("Animes\\" + title + ".txt", "w")
        except OSError:
            file = open("Animes\\INVALID NAME.txt", "w")
        file.write(text)
        if title in valid_anime_list:
            if title not in downloaded_animes:
                download_count += 1
                downloader(link_list, c)
                print(str((len(downloaded_anime_name)+1)) + " - downloading       :" + title)
            else:
                print(str((len(downloaded_anime_name)+1)) + " - not downloading   :" + title)
            downloaded_anime_name.append(title)
            
                

    text = ""
    count = 0
    while True:
        try:
            text += str(downloaded_anime_name[count]) + "\n"
            count += 1
        except IndexError:
            file = open("recently downloaded animes.txt", "w")
            file.write(text)
            file.close()
            break
                                                 
    input( "--------------------------------------------------------------"+
          "\n" +str(download_count)+ " anime are downloading via torrent... Press Enter to continue. ..")

def download(list_1):
    webbrowser.open(str(list_1[0]))


def downloader(magnet_list, choice):
    start = 0
    if len(magnet_list) == 39:
        start += 3
    magnet_links_480 = [magnet_list[start].get("href")]
    magnet_links_720 = [magnet_list[start+1].get("href")]
    magnet_links_1080 = [magnet_list[start+2].get("href")]
    while True:
        if choice == "1":
            download(magnet_links_480)
            break
        elif choice == "2":
            download(magnet_links_720)
            break
        elif choice == "3":
            download(magnet_links_1080)
            break
        elif choice == "4":
            break
        else:
            print("Option not available")
            break


def choice_getter():
    while True:
        print("1 - 480p\n2 - 720p\n3 - 1080p\n4 - Exit")
        choice = input("In which quality do you want to download the Anime :")
        if choice == "1" or "2" or "3" or "4":
            break
        else:
            print("Option not available")
    return choice


valid_anime_list = []
downloaded_animes = []


valid_anime_check()
downloaded_anime_check()

create_and_save()

