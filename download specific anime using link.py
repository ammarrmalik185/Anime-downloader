from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser


def url_to_sourcecode(url):
    driver = webdriver.Chrome()
    driver.get(url)
    code = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return code


def source_code_info_getter(source_code):
    title = source_code.findAll("h1", {"class": "entry-title"})
    magnet_links = source_code.findAll("a", {"title": "Magnet Link"})
    episode_nos = source_code.findAll("div", {"class": "rls-info-container"})
    episode_no_list = []
    for element in episode_nos:
        episode_no = element.get("id")
        episode_no_list.append(episode_no)

    return magnet_links, episode_no_list


def choice_getter():
    while True:
        print("1 - 480p\n2 - 720p\n3 - 1080p\n4 - Exit")
        choice = input("In which quality do you want to download the Anime :")
        if choice == "1" or "2" or "3" or "4":
            break
        else:
            print("Option not available")
    return choice

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



def main():
    print("NOTE : This will only download lastest 12 episodes of the designated anime")
    url = input("Enter the url :")
    source_code = url_to_sourcecode(url)
    magnet_links, episode_no_list = source_code_info_getter(source_code)
    c = choice_getter()
    downloader(c, magnet_links)

main()
