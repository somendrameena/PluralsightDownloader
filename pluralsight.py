# Standard Python Imports
from argparse import Namespace
import os
import time
import requests

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Third-party libraries imports
from slugify import slugify
from clint.textui import progress

# Imports within project
import config


class PluralSight:
    # CSS Selector
    CONSTANTS_CSS_SELECTOR = dict(
        LOGIN_BUTTON=".button.flat.white.header_sign_in_link.sign_in_link",
        EXPAND_BUTTON=".buttonLink---KymJM",
        TABLE_OF_CONTENTS=".clipListTitle---hbKca",
        MODULES_LIST=".module",
        MODULE_NAME=".m-0.p-0.ps-color-white.ps-type-sm.ps-type-weight-medium",
        MODULE_EXPAND_BUTTON=".ps-color-gray-02.ps-type-lg.align-self-center.p-md.icon-drop-down",
        LECTURES=".m-0.p-0.ps-type-xs.ps-type-weight-book.side-menu-clip-title.ps-type-ellipsis",
    )

    # ID
    CONSTANTS_ID = dict(
        USERNAME="Username",
        PASSWORD="Password",
        LOGIN="login",
    )

    # Tag Name
    CONSTANTS_TAG_NAME = dict(
        VIDEO="video"
    )

    # Attribute
    CONSTANTS_ATTRIBUTE = dict(
        SOURCE="src"
    )

    CONSTANTS_LOG_MESSAGES = dict(
        LOGIN_ELEMENT_NOT_FOUND="NoSuchElementException in login()",
        DOWNLOAD_ELEMENT_NOT_FOUND="NoSuchElementException in download_lectures()",
        NO_VIDEO_PLAYED="No video is being played.",
        ALREADY_DOWNLOADED="Already downloaded ... skipping \n",
        ALREADY_EXPANDED=" is already expanded",
    )

    CSS_SELECTOR = Namespace(**CONSTANTS_CSS_SELECTOR)
    ID = Namespace(**CONSTANTS_ID)
    TAG_NAME = Namespace(**CONSTANTS_TAG_NAME)
    ATTRIBUTE = Namespace(**CONSTANTS_ATTRIBUTE)
    LOG_MESSAGES = Namespace(**CONSTANTS_LOG_MESSAGES)

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(config.link)

    def login(self):
        try:
            login_button = self.browser.find_element_by_css_selector(self.CSS_SELECTOR.LOGIN_BUTTON)
            login_button.click()
            time.sleep(5)

            username_field = self.browser.find_element_by_id(self.ID.USERNAME)
            username_field.send_keys(config.username)
            password_field = self.browser.find_element_by_id(self.ID.PASSWORD)
            password_field.send_keys(config.password)
            login_button = self.browser.find_element_by_id(self.ID.LOGIN)
            login_button.click()
            time.sleep(3)
        except NoSuchElementException:
            print(self.LOG_MESSAGES.LOGIN_ELEMENT_NOT_FOUND)

    def get_video_url(self):
        try:
            video_container = self.browser.find_element_by_tag_name(self.TAG_NAME.VIDEO)
            return video_container.get_attribute(self.ATTRIBUTE.SOURCE)
        except NoSuchElementException:
            print(self.LOG_MESSAGES.NO_VIDEO_PLAYED)
            return None

    def download(self, path):
        if not os.path.exists(path):
            video_url = self.get_video_url()
            if video_url:
                r = requests.get(video_url, stream=True)
                with open(path, 'wb') as f:
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()
        else:
            print(self.LOG_MESSAGES.ALREADY_DOWNLOADED)

    def download_lectures(self):
        try:
            expand_button = self.browser.find_element_by_css_selector(self.CSS_SELECTOR.EXPAND_BUTTON)
            expand_button.click()

            self.browser.find_element_by_css_selector(self.CSS_SELECTOR.TABLE_OF_CONTENTS).click()

            # Switch Tab
            self.browser.switch_to.window(self.browser.window_handles[1])

            time.sleep(5)
            course_name = self.browser.title

            modules = self.browser.find_elements_by_css_selector(self.CSS_SELECTOR.MODULES_LIST)

            modules_count = 0
            for module in modules:

                modules_count = modules_count + 1
                module_name = module.find_element_by_css_selector(self.CSS_SELECTOR.MODULE_NAME).text
                module_dir_name = course_name + "/" + str(modules_count) + "." + module_name
                if not os.path.exists(module_dir_name):
                    os.makedirs(module_dir_name)

                try:
                    module_expand_button = module.find_element_by_css_selector(self.CSS_SELECTOR.MODULE_EXPAND_BUTTON)
                    module_expand_button.click()
                except NoSuchElementException:
                    print(module_name + self.LOG_MESSAGES.ALREADY_EXPANDED)

                lectures = module.find_elements_by_css_selector(self.CSS_SELECTOR.LECTURES)

                lectures_count = 0
                for lecture in lectures:
                    lecture.click()

                    lectures_count = lectures_count + 1
                    lecture_dir_name = module_dir_name + "/" + str(lectures_count) + "." + slugify(
                        lecture.text) + ".mp4"

                    time.sleep(3)

                    # pausePlayback()
                    self.browser.find_element_by_css_selector("body").send_keys(Keys.SPACE)

                    print(module_name + " | " + lecture.text)
                    self.download(lecture_dir_name)

        except NoSuchElementException:
            print(self.LOG_MESSAGES.DOWNLOAD_ELEMENT_NOT_FOUND)


if __name__ == '__main__':
    ps = PluralSight()
