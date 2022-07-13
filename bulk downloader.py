from bs4 import BeautifulSoup
from selenium import webdriver
import os
import webbrowser
import time


def get_data():
    url = input("Enter URL :")
    driver = webdriver.Chrome()
    driver.get(url)
    while True:
        try:
            time.sleep(3)
            driver.find_element_by_link_text("Show more ▼").click()
            time.sleep(1)
        except :
            break
        
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def parse(data):
    comp_links = []
    for container in data.findAll("div",{"class":"rls-info-container"}):
        links = []
        for link_cont in container.findAll("a",{"title":"Magnet Link"}):
            link = link_cont["href"]
            links.append(link)
        comp_links.append(links)

            
    return comp_links


def choice_getter():
    while True:
        print("1 - Lowest(360p or 480p)\n2 - Medium(720p)\n3 - High(1080p)")
        choice = input("In which quality do you want to download the Anime :")
        if choice == "1" or "2" or "3":
            break
        else:
            print("Option not available")
    return choice


def core():
    try:
        comp_links = parse(get_data())
        choice = choice_getter()
        count = 0
        for links in comp_links:
            webbrowser.open(str(links[int(choice) - 1]))
            count += 1

        input(str(count) + " files downloading... press enter to continue...")
            
    except AttributeError:
        input("Internet not available ... press enter to continue")

core()
