from bs4 import BeautifulSoup
from selenium import webdriver
import os
import webbrowser

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

    return text, title, magnet_links



def shows_page_links():
    links = []
    titles = []
    url = r"https://horriblesubs.info/shows/"
    url2 = r"https://horriblesubs.info"
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    link_pack = soup.findAll("div", {"class":"ind-show"})
    for element in link_pack:
        list = element.findAll("a", {"":""})
        link = url2 + list[0].get("href")
        title = list[0].get("title")
        links.append(link)
        titles.append(title)

    return links, titles


def main():
    print("NOTE : This will only download lastest 12 episodes of the designated anime")
    name = input("Enter the name of the Anime :")
    links, titles = shows_page_links()
    if name in titles:
        index = titles.index(name)
        link = links[index]
        code_list = link_source_code_getter([link])
        text, title, links = source_code_info_getter(code_list[0])
        if not os.path.exists("Specifically Downloaded Animes\\"):
            os.makedirs("Specifically Downloaded Animes\\")
        file = open("Specifically Downloaded Animes\\" + title + ".txt", "w")
        file.write(text)
        file.close()
        c = choice_getter()
        downloader(c, links)
    else:
        print("Anime not found")
        input()


def open_links(links):
    for link in links:
        webbrowser.open(str(link.get("href")))


def downloader(choice, magnet_links):
    start_1 = 0
    start_2 = 1
    start_3 = 2
    magnet_480 = []
    magnet_720 = []
    magnet_1080 = []

    if len(magnet_links) == 39:
        start_1 += 3
        start_2 += 3
        start_3 += 3

    while True:
        try:
            magnet_480.append(magnet_links[start_1])
            magnet_720.append(magnet_links[start_2])
            magnet_1080.append(magnet_links[start_3])
            start_1 += 3
            start_2 += 3
            start_3 += 3
        except IndexError:
            break

    if choice == "1":
        open_links(magnet_480)
    elif choice == "2":
        open_links(magnet_720)
    elif choice == "3":
        open_links(magnet_1080)
    elif choice == "4":
        print("Exiting without downloading")


def choice_getter():
    while True:
        print("1 - 480p\n2 - 720p\n3 - 1080p\n4 - Exit")
        choice = input("In which quality do you want to download the Anime :")
        if choice == "1" or "2" or "3" or "4":
            break
        else:
            print("Option not available")
    return choice

main()
