
from bs4 import BeautifulSoup
from selenium import webdriver
import os


def get_html_text_main_page():
    driver = webdriver.Chrome()
    url = "https://myanimelist.net/anime/season"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def code_to_links_main(code):
    link_list = []
    code = code.find("div", {"class": "seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix"})
    for x in code.findAll("div", {"class": "seasonal-anime js-seasonal-anime"}):
        y = x.find("a", {"class": "link-title"})
        link = y.get('href')
        link = str(link)
        link_list.append(link)

    return link_list


def get_html_text_se_page(links):
    source_codes = []
    driver = webdriver.Chrome()
    for link in links:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        source_codes.append(soup)
    driver.quit()
    return source_codes


def code_to_info_get(code):
    for x in code.findAll("div", {"class": "spaceit"}):
        text = x.get_text()
        print(text + "\n")


def get_names_fast(code):
    if not os.path.exists(r"C:\Users\ParadoX\PycharmProjects\Web Crawler v 3.0\New Season Animes"):
        os.makedirs(r"C:\Users\ParadoX\PycharmProjects\Web Crawler v 3.0\New Season Animes")

    file = open(r"C:\Users\ParadoX\PycharmProjects\Web Crawler v 3.0\New Season Animes\New Animes.txt", "w")
    tv_series = code.find("div", {"class": "seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix"})
    for x in tv_series.findAll("div", {"class": "seasonal-anime js-seasonal-anime"}):
        y = x.find("a", {"class": "link-title"})
        text = y.get_text()
        try:
            file.write(text + "\n")
        except UnicodeEncodeError:
            file.write("UnicodeEncodeError: UNABLE TO DECODE NAME\n")
get_names_fast(get_html_text_main_page())
        

