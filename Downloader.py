from selenium import webdriver
from selenium import common
from bs4 import BeautifulSoup
import time
import webbrowser
import os


class Test:
    def __init__(self):
        self.sep = "<EP>"
        self.valid_anime_list = []
        self.downloaded_animes = []
        self.downloaded_animes_ep = []

    def downloaded_anime_check(self):
        if os.path.isfile(r"cache(beta)\recently downloaded animes.txt"):
            file = open(r"cache(beta)\recently downloaded animes.txt", "r")
            for line in file.readlines():
                if "\n" in line:
                    line = line.replace("\n", "")
                parts = line.split(self.sep)
                self.downloaded_animes.append(parts[0].lower())
                self.downloaded_animes_ep.append(parts[1].lower())
        else:
            open(r"cache(beta)\recently downloaded animes.txt", "w")

    def valid_anime_check(self):
        if os.path.isfile(r"cache(beta)\valid animes.txt"):
            file = open(r"cache(beta)\valid animes.txt", "r")
            for line in file.readlines():
                if "\n" in line:
                    line = line.replace("\n", "")
                if line != "" and line != " ":
                    self.valid_anime_list.append(line.lower())
        else:
            open(r"cache(beta)\valid animes.txt", "w")


class Downloader:

    def __init__(self, validanimes, invalidanimes, invalideps, silent):

        self.validAnimes = validanimes
        self.downloaded = invalidanimes
        self.downloaded_eps = invalideps

        self.check_complex = []
        self.notDownload = {}
        self.yesDownload = {}
        self.details = {}
        self.link_set = {}
        self.errors = []

        self.url = "https://horriblesubs.info"
        self.delay = 1

        self.download = True
        self.print = True
        self.constraint = True
        self.force_download = False
        self.force_res = False
        self.silent = silent

        self.chrome_elements = webdriver.ChromeOptions()
        self.chrome_elements.add_argument('log-level=3')
        if self.silent:
            self.chrome_elements.add_argument('--headless')

    def print_all(self):
        print(self.validAnimes)
        print(self.downloaded)
        print(self.downloaded_eps)

        print(self.yesDownload)
        print(self.notDownload)
        print(self.details)
        print(self.link_set)

        print(self.url)

        print(self.download)
        print(self.print)
        print(self.constraint)
        print(self.force_download)

    def merge(self):
        for i in range(len(self.downloaded)):
            self.check_complex.append(str(self.downloaded[i]) + str(self.downloaded_eps[i]))

    def get_main_page(self):

        driver = webdriver.Chrome(chrome_options=self.chrome_elements)
        driver.get(self.url)

        source_1 = driver.page_source
        while True:
            try:
                button = driver.find_element_by_link_text("Show more ▼")
                button.click()
                while True:
                    if driver.page_source != source_1:
                        try:
                            source_1 = driver.page_source
                            time.sleep(1)
                            break
                        except common.exceptions.ElementClickInterceptedException:
                            time.sleep(1)
                        except common.exceptions.StaleElementReferenceException:
                            time.sleep(1)
                    else:
                        time.sleep(1)
            except common.exceptions.NoSuchElementException:
                break
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup

    def get_links(self, code):
        self.details = {}

        code = code.find("div", {"class": "latest-releases"})

        for e in code.findAll("li", {}):
            span = e.find("span", {"class": "latest-releases-date"})
            strong = e.find("strong", {})
            div = e.find("div", {})
            a = e.find("a", {})

            link = a["href"]
            link = self.url + link
            resolutions = div.get_text()
            release_date = span.get_text()
            episode_no = strong.get_text()

            complete = e.get_text()

            episode_name = complete[::-1].replace(resolutions[::-1], "", 1)[::-1]
            episode_name = episode_name[::-1].replace(release_date[::-1], "", 1)[::-1]
            episode_name = episode_name[::-1].replace(episode_no[::-1], "", 1)[::-1]
            episode_name = episode_name[:-3]

            self.details[complete] = [episode_name, episode_no, link, release_date, True]

    '''
    def filter(self): (old)
        self.merge()
        if self.constraint:
            for detail in self.details:
                if self.details[detail][0].lower() not in self.validAnimes:
                    self.details[detail][4] = False
        if not self.force_download:
            for detail in self.details:
                if self.details[detail][0].lower() in self.downloaded:
                        if self.details[detail][1] == \
                                self.downloaded_eps[self.downloaded.index(self.details[detail][0].lower())]:
                            self.downloaded[self.downloaded.index(self.details[detail][0].lower())] = None
                            self.notDownload[detail] = self.details[detail]
                            self.details[detail][4] = False
                        else:
                            self.yesDownload[detail] = self.details[detail]
                else:
                    if self.details[detail][4] is not False:
                        self.yesDownload[detail] = self.details[detail]
    '''

    def filter(self):
        self.merge()
        if self.constraint:
            for detail in self.details:
                if self.details[detail][0].lower() not in self.validAnimes:
                    self.details[detail][4] = False
        if not self.force_download:
            for detail in self.details:
                if self.details[detail][0].lower() + self.details[detail][1] in self.check_complex:
                        self.downloaded[self.downloaded.index(self.details[detail][0].lower())] = None
                        self.notDownload[detail] = self.details[detail]
                        self.details[detail][4] = False
                else:
                    if self.details[detail][4] is not False:
                        self.yesDownload[detail] = self.details[detail]

    def link_set_maker(self):
        for detail in self.details:
            if self.details[detail][-1]:
                if not self.details[detail][0] in self.link_set:
                    self.link_set[self.details[detail][0]] = [self.details[detail][2],
                                                              [self.details[detail][1]], [], []]
                else:
                    self.link_set[self.details[detail][0]][1].append(self.details[detail][1])

    @staticmethod
    def choice_getter():
            while True:
                print("1 - Lowest(360p or 480p)\n2 - Medium(720p)\n3 - High(1080p)\n4 - Exit")
                choice = input("In which quality do you want to download the Anime :")
                if choice == "1" or "2" or "3" or "4":
                    break
                else:
                    print("Option not available")
            return choice

    def download_link_append(self):

        if self.force_res is False:
            choice = self.choice_getter()
        else:
            choice = 1
        if choice != "4":
            driver = webdriver.Chrome(chrome_options=self.chrome_elements)
            for link in self.link_set:
                driver.get(self.link_set[link][0])
                page_source = BeautifulSoup(driver.page_source, features='html.parser')
                for ep in self.link_set[link][1]:
                    ep_link = ''
                    bol_error = False
                    ep = ep.replace('.', '-')
                    div_element = page_source.find('div', {'id': ep})
                    while True:
                        if div_element is None:
                            time.sleep(self.delay)
                            page_source = BeautifulSoup(driver.page_source, features='html.parser')
                            div_element = page_source.find('div', {'id': ep})
                            self.errors.append("Error loading page with id : " + link)
                        else:
                            break

                    if self.force_res == 360:
                        ep_link = div_element.find('div', {'class': 'rls-link link-360p'})
                        if ep_link is None:
                            bol_error = True
                            self.errors.append(link + ' - episode - ' + ep + ' not found in 360p')
                        else:
                            ep_link = ep_link.find('a', {'title': 'Magnet Link'})
                            ep_link = ep_link.get('href')
                    elif self.force_res == 480:
                        ep_link = div_element.find('div', {'class': 'rls-link link-480p'})
                        if ep_link is None:
                            bol_error = True
                            self.errors.append(link + ' - episode - ' + ep + ' not found in 480p')
                        else:
                            ep_link = ep_link.find('a', {'title': 'Magnet Link'})
                            ep_link = ep_link.get('href')
                    elif self.force_res == 720:
                        ep_link = div_element.find('div', {'class': 'rls-link link-720p'})
                        if ep_link is None:
                            bol_error = True
                            self.errors.append(link + ' - episode - ' + ep + ' not found in 720p')
                        else:
                            ep_link = ep_link.find('a', {'title': 'Magnet Link'})
                            ep_link = ep_link.get('href')
                    elif self.force_res == 1080:
                        ep_link = div_element.find('div', {'class': 'rls-link link-1080p'})
                        if ep_link is None:
                            bol_error = True
                            self.errors.append(link + ' - episode - ' + ep + ' not found in 1080p')
                        else:
                            ep_link = ep_link.find('a', {'title': 'Magnet Link'})
                            ep_link = ep_link.get('href')
                    else:

                        links = div_element.findAll('a', {'title': 'Magnet Link'})
                        if choice == "1":
                            ep_link = links[0].get('href')
                        elif choice == "2":
                            ep_link = links[1].get('href')
                        elif choice == "3":
                            ep_link = links[2].get('href')

                    self.link_set[link][2].append(ep_link)
                    self.link_set[link][3].append(bol_error)
            driver.quit()
        else:
            pass

    def return_values(self):
        return [self.notDownload, self.details, self.yesDownload, self.errors]

    def download_all(self):
        done = []
        done_ep = []
        for link in self.link_set:
            for i in range(0, len(self.link_set[link][3])):
                if not self.link_set[link][3][i]:
                    webbrowser.open(self.link_set[link][2][i])
                    done.append(link)
                    done_ep.append(self.link_set[link][1][i])

        return done, done_ep


def test():
    source = Test()

    source.downloaded_anime_check()

    source.valid_anime_check()

    print(source.downloaded_animes)
    print(source.downloaded_animes_ep)

    crawler = Downloader(source.valid_anime_list, source.downloaded_animes, source.downloaded_animes_ep)

    crawler.get_links(crawler.get_main_page())

    crawler.filter()

    crawler.link_set_maker()

    print(crawler.downloaded)

    crawler.download_link_append()

    for x in crawler.return_values():
        print(x)


class EasyDownloader:
    def __init__(self, validanimes, downloadedan, downloadedeps):
        crawler = Downloader(validanimes, downloadedan, downloadedeps)
        self.force_res = False

        crawler.force_res = self.force_res

        crawler.get_links(crawler.get_main_page())

        crawler.filter()

        crawler.link_set_maker()

        self.info = crawler.return_values()

    def get_values_1(self):
        return self.info
