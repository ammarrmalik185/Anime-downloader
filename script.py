from selenium import webdriver
from idm import IDMan

driver = webdriver.Chrome()
downloader = IDMan()

driver.get("https://animekisa.tv/")

driver.find_element_by_tag_name("").get_attribute("href")

anime_boxes = driver.find_elements_by_class_name('episode-box')

anime_links = []
for anime in anime_boxes:
    link = anime.find_element_by_tag_name('a').get_attribute("href")
    anime_links.append(link)


def download_from_link(url):
    driver.get(url)
    button = driver.find_element_by_class_name('server_button_l')
    button.click()
    driver.switch_to.window(driver.window_handles[1])

    download_links = {}
    name = driver.find_element_by_id('title').text
    link_containers = driver.find_elements_by_class_name('dowload')
    for linkContainer in link_containers:
        link_title = linkContainer.text
        link_url = linkContainer.find_element_by_tag_name('a').get_attribute('href')
        download_links[link_title] = link_url

    link = download_links['DOWNLOAD (360P - MP4)']
    downloader.download(link, 'c:/test', output=name + ".mp4")




