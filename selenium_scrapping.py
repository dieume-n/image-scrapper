import re
import os
import time
from selenium import webdriver


class FirefoxScrapper:
    def __init__(self):
        self.driver = webdriver.Firefox(
            executable_path="./browser/geckodriver.exe")
        self.wait = 10
        self.driver.implicitly_wait(self.wait)

    def extract_images(self):
        self.driver.find_elements_by_tag_name('img')

    def scrappe(self, url):
        self.driver.get(url)
