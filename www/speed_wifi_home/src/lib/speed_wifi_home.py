#!/usr/bin/env python

import os
import re
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from typing import Tuple

LoginInfo = Tuple[str, str, str]


class SpeedWifiHome:
    def __init__(self, driver: str = '/usr/pkg/bin/geckodriver') -> None:
        self.__check_file_path(driver)
        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Firefox(
            executable_path=driver,
            options=options
        )

    def __check_str(self, arg) -> None:
        if type(arg) is not str:
            raise TypeError

    def __check_file_path(self, path: str) -> None:
        self.__check_str(path)
        if not os.path.exists(path):
            raise FileNotFoundError

    def parse_conf(self, conf: str) -> LoginInfo:
        self.__check_file_path(conf)
        with open(conf, mode='r', encoding='utf-8') as f:
            login = yaml.safe_load(f)
        return login['address'], login['username'], login['password']

    def login(self, address: str, username: str, password: str) -> None:
        for arg in address, username, password:
            self.__check_str(arg)
        if not re.match(r'^http[s]{0,1}://', address):
            url = 'http://' + address
        else:
            url = address
        if not re.match(r'/html/login.htm$', address):
            url += '/html/login.htm'
        self.browser.get(url)
        self.browser.find_element_by_id('user_type').send_keys(username)
        self.browser.find_element_by_id('input_password').send_keys(password)
        self.browser.find_element_by_id('login').click()

    def get_traffic_of_last_three_days(self) -> str:
        current = self.browser.current_url.split('/')
        del current[-1]
        url = '/'.join(current) + '/statistics.htm'
        print(url)
        self.browser.get(url)
        ret = self.browser.page_source
        self.__check_str(ret)
        return ret
