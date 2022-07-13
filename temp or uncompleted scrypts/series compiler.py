from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

search = input("Enter Query :")
driver = webdriver.Chrome()

path = "series compiler data/"

if not os.path.exists(path):
        os.makedirs(path)


no = 1
while True:
    name = search + " " + str(no) + ".txt"
    if not os.path.isfile(path + name):
        file = open(path + name,"w",encoding="utf-8")
        break
    no += 1
        



def initial():
    
    search.replace(" ","%20", 100)
    url = "https://myanimelist.net/anime.php?q="
    url = url + search
    driver.get(url)
    return BeautifulSoup(driver.page_source, features="html.parser")

def parse_main(code):
    links =  []
    for x in code.findAll("a" ,{"class" : "hoverinfo_trigger fw-b fl-l"}):
        link = x.get("href")
        links.append(link)

    return links

def looper(links):
    control = 1000
    iteration = 1
    for link in links:
        driver.get(link)
        name = driver.find_element_by_xpath('//*[@id="contentWrapper"]/div[1]/h1/span')       
        try:
            file.write(name.text + "\n")
        except UnicodeEncodeError:
            file.write("unicode error \n")
            
        info = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/div')
        info = info.text.replace("\n\n","\n",100).split("\n")[2:]
        print_bol = True
        
        for i in info:
            if print_bol:
                file.write(i + "\n")
            if "Information" in i:
                print_bol = True
                
        time.sleep(2)
        file.write("\n\n------------------------------\n\n")
        if control <= iteration:
            break
        iteration  += 1
        print(name.text + "  done")
        print("total " + str(iteration-1) + " animes recorded")

temp = parse_main(initial())
looper(temp)

driver.quit()
file.close()
