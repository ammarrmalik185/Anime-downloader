from selenium import webdriver
from selenium import common
from idm import IDMan
from datetime import datetime


class Options:

    def __init__(self, silent=True, quality=None, confirmation=False, logs=False,
                 alternate_quality=True, download_path="\\animes", pages_to_scan=1, auto_exit=False,
                 auto_exception_control=True, max_refresh_page=5, generate_log_file=True):
        if quality is None:
            quality = {"type": "force_res", "value": "720p"}
        self.silent = silent
        self.confirmation = confirmation
        self.logs = logs
        self.quality = quality
        self.alternate_quality = alternate_quality
        self.download_path = download_path
        self.pages_to_scan = pages_to_scan
        self.auto_exit = auto_exit
        self.auto_exception_control = auto_exception_control
        self.max_refresh_page = max_refresh_page
        self.generate_log_file = generate_log_file


class Crawler:
    def __init__(self,  anime_data, options=Options()):
        self.options = options

        self.valid_animes = anime_data[0]
        self.already_downloaded_animes = anime_data[1]
        self.already_downloaded_eps = anime_data[2]

        self.chrome_options = None
        self.driver = None
        self.initialize_driver()

        self.downloader = IDMan()

        # anime_data = [{"name", "ep_no", "link"}]
        # complete_anime_data = [{"name", "ep_no", "page_link", "download_link", "file_name", "status"}]

        self.downloading = []         # in anime_data_list format
        self.not_downloading = []     # in anime_data_list format
        self.not_valid = []           # in anime_data_list format

        self.complete_data = []       # in complete_anime_data format
        self.unable_to_find = []      # in complete_anime_data format

        self.errors = []              # string array
        self.logs = []                # string array

        # log
        statement = "Valid Animes: "
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        for anime in self.valid_animes:
            statement = "\t\t" + anime
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)
        statement = "Already Downloaded Animes: "
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        for i in range(len(self.already_downloaded_animes)):
            statement = "\t\t" + self.already_downloaded_animes[i] + ", EP: " + self.already_downloaded_eps[i]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)

    def initialize_driver(self):
        self.chrome_options = webdriver.ChromeOptions()
        if not self.options.logs:
            self.chrome_options.add_argument('log-level=3')
        if self.options.silent:
            self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.set_page_load_timeout(30)

    def get_initial_data(self):
        anime_data = self.get_initial_data_from_url("https://animekisa.tv/")

        for i in range(1, self.options.pages_to_scan):
            anime_data = anime_data + self.get_initial_data_from_url("https://animekisa.tv/latest/" + str(i))

        return anime_data

    def get_initial_data_from_url(self, url):
        self.driver.get(url)
        anime_boxes = self.driver.find_elements_by_class_name('episode-box')

        anime_data = []
        for box in anime_boxes:
            name = box.find_element_by_class_name("title-box-2").text
            link = box.find_element_by_tag_name('a').get_attribute("href")
            temp = link.split("-")
            ep_no = temp[len(temp) - 1]

            anime_data.append({"name": name, "link": link, "ep_no": ep_no})

        return anime_data

    def filter_anime_data(self, anime_data):

        anime_to_download = []
        found_but_not_downloading = []
        invalid_animes = []

        # log
        statement = "Filtering the following animes: "
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)

        for anime in anime_data:
            valid = False
            downloaded = False

            # log
            statement = "\t\t" + anime["name"] + ", EP: " + anime["ep_no"]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)

            if anime["name"].lower() in self.valid_animes:
                valid = True

            if (anime["name"].lower() in self.already_downloaded_animes) and (anime["ep_no"] ==
                    self.already_downloaded_eps[self.already_downloaded_animes.index(anime["name"].lower())]):
                downloaded = True

            if valid:
                if downloaded:
                    found_but_not_downloading.append(anime)
                else:
                    anime_to_download.append(anime)
            else:
                invalid_animes.append(anime)

        return anime_to_download, found_but_not_downloading, invalid_animes

    def get_download_link_per_anime(self, link):
        try:
            self.driver.get(link)
        except common.exceptions.InvalidSessionIdException:
            self.initialize_driver()
            self.driver.get(link)
        button = self.driver.find_element_by_class_name('server_button_l')
        button.click()

        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to.window(handles[1])

        download_links = {}
        name = self.driver.find_element_by_id('title').text

        link_containers = self.driver.find_element_by_class_name("mirror_link").find_elements_by_class_name('dowload')
        for linkContainer in link_containers:
            link_title = linkContainer.text
            link_url = linkContainer.find_element_by_tag_name('a').get_attribute('href')
            download_links[link_title] = link_url

        link, status = self.choose_from_quality(download_links)
        name = name.replace(":", " -") + ".mp4"

        return name, link, status

    def choose_from_quality(self, qualities):
        if self.options.quality["type"] == "force_res":
            if self.options.quality["value"] == "360p":
                if 'DOWNLOAD (360P - MP4)' in qualities:
                    return qualities['DOWNLOAD (360P - MP4)'], "200"
                else:
                    if not self.options.alternate_quality:
                        return 'none', "404"

            elif self.options.quality["value"] == "480p":
                if 'DOWNLOAD (480P - MP4)' in qualities:
                    return qualities['DOWNLOAD (480P - MP4)'], "200"
                else:
                    if not self.options.alternate_quality:
                        return 'none', "404"

            elif self.options.quality["value"] == "720p":
                if 'DOWNLOAD (720P - MP4)' in qualities:
                    return qualities['DOWNLOAD (720P - MP4)'], "200"
                else:
                    if not self.options.alternate_quality:
                        return 'none', "404"

            elif self.options.quality["value"] == "1080p":
                if 'DOWNLOAD (1080P - MP4)' in qualities:
                    return qualities['DOWNLOAD (1080P - MP4)'], "200"
                else:
                    if not self.options.alternate_quality:
                        return 'none', "404"

            elif self.options.quality["value"] == "source":
                if 'DOWNLOAD (HDP - MP4)' in qualities:
                    return qualities['DOWNLOAD (HDP - MP4)'], "200"
                else:
                    if not self.options.alternate_quality:
                        return 'none', "404"

            else:
                return 'none', "404"

        elif self.options.quality["type"] == "comparative":
            if self.options.quality["value"] == "best":
                return qualities[qualities.keys()[0]], "200"

            elif self.options.quality["value"] == "worst":
                return qualities[qualities.keys()[len(qualities)]], "200"

        if self.options.quality["type"] == "force_res" and self.options.alternate_quality:
            if 'DOWNLOAD (HDP - MP4)' in qualities:
                return qualities['DOWNLOAD (HDP - MP4)'], "200"
            else:
                return "none", "404"

    def start_part_1(self):
        initial_data = self.get_initial_data()

        # log
        statement = "no of all animes: " + str(len(initial_data))
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)

        self.downloading, self.not_downloading, self.not_valid = self.filter_anime_data(initial_data)

        # log
        statement = "downloading :" + str(len(self.downloading)) + " - already downloading :" +\
                    str(len(self.not_downloading)) + " - not valid :" + str(len(self.not_valid))
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        statement = "Anime to download :"
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        for anime in self.downloading:
            statement = "\t\t" + anime["name"] + ", EP: " + anime["ep_no"]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)
        statement = "Anime that have already been downloaded :"
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        for anime in self.not_downloading:
            statement = "\t\t" + anime["name"] + ", EP: " + anime["ep_no"]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)
        statement = "Anime that are not valid :"
        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
        if self.options.logs:
            print(statement)
        for anime in self.not_valid:
            statement = "\t\t" + anime["name"] + ", EP: " + anime["ep_no"]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)

    def get_mid_term_data(self):
        return self.downloading, self.not_downloading, self.not_valid, self.errors

    def start_part_2(self):
        for anime_data in self.downloading:
            success = [False]

            # log
            statement = "Attempting to find the download link for the anime: " + anime_data["name"] + ", url: " + \
                        anime_data["link"]
            self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
            if self.options.logs:
                print(statement)
            for exception_count in range(self.options.max_refresh_page):
                try:
                    file_name, download_link, status = self.get_download_link_per_anime(anime_data["link"])
                    if status == "200":
                        self.complete_data.append({
                            "name": anime_data["name"],
                            "ep_no": anime_data["ep_no"],
                            "page_link": anime_data["link"],
                            "file_name": file_name,
                            "download_link": download_link,
                            "status": status
                        })

                        # log
                        statement = "The download link for the anime: " + anime_data["name"] + ", url: " + \
                                    anime_data["link"] + " was found successfully, the link is: " + download_link
                        self.logs.append("[" + str(datetime.now().time()) + "]:" + statement)
                        if self.options.logs:
                            print(statement)

                    elif status == "404":
                        self.unable_to_find.append({
                            "name": anime_data["name"],
                            "ep_no": anime_data["ep_no"],
                            "page_link": anime_data["link"],
                            "file_name": file_name,
                            "download_link": download_link,
                            "status": status
                        })

                        # log - exception
                        exception_statement = "Unable to find anime: " + anime_data["name"] + ", url: " +\
                            anime_data["link"] + " in the specified quality"
                        self.errors.append(exception_statement)
                        self.logs.append("[" + str(datetime.now().time()) + "]:" + exception_statement)
                        if self.options.logs:
                            print(exception_statement)

                    success[0] = True
                    break
                except Exception as ex:
                    if not self.options.auto_exception_control:
                        self.save_logs()
                        raise ex

                    # log - exception
                    exception_statement = "Error occurred loading page of anime: " + anime_data["name"] + ", url: " +\
                        anime_data["link"] + ", error: " + str(ex.args[0]) + ", trying again attempt no :" + \
                        str((exception_count+1)) + " out of " + str(self.options.max_refresh_page)
                    self.errors.append(exception_statement)
                    self.logs.append("[" + str(datetime.now().time()) + "]:" + exception_statement)
                    if self.options.logs:
                        print(exception_statement)

            if not success[0]:
                self.unable_to_find.append({
                    "name": anime_data["name"],
                    "ep_no": anime_data["ep_no"],
                    "page_link": anime_data["link"],
                    "file_name": "404",
                    "download_link": "404",
                    "status": "504"
                })

                # log - exception
                exception_statement = "Max page refresh failed for the anime: " + anime_data["name"] + ", url: " + \
                                      anime_data["link"] + ". It cannot be downloaded"
                self.errors.append(exception_statement)
                self.logs.append("[" + str(datetime.now().time()) + "]:" + exception_statement)
                if self.options.logs:
                    print(exception_statement)

    def get_end_term_data(self):
        return self.complete_data, self.unable_to_find, self.errors

    def get_save_data(self):
        download = []
        download_ep = []

        for data in self.complete_data:
            download.append(data["name"])
            download_ep.append(data["ep_no"])

        for data in self.not_downloading:
            download.append(data["name"])
            download_ep.append(data["ep_no"])

        return [download, download_ep]

    def download_animes(self):
        for anime in self.complete_data:
            self.downloader.download(anime["download_link"],
                                     self.options.download_path,
                                     output=anime["file_name"],
                                     confirm=self.options.confirmation)

    def save_logs(self):
        if self.options.generate_log_file:
            log_file = open("core.log", "w", encoding="UTF-8")
            for log in self.logs:
                log = log.replace(r"\n", r"\\n")
                log_file.write(log + "\n")
            log_file.write("[" + str(datetime.now().time()) + "]:" + "Execution Completed Successfully")
            log_file.close()

    def close_crawler(self):
        self.save_logs()
        self.driver.quit()
