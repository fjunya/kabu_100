from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from django.conf import settings

driver_path = "./tmp/driver/geckodriver"

class Command(BaseCommand):
    help = ''
    driver = webdriver.Firefox(executable_path=driver_path)

    def handle(self, *args, **options):
        self.download()

    def download(self):
        #Yahoo login
        LOGIN_URL = settings.LOGIN_URL
        USER_ID = settings.USER_ID
        PASSWORD = settings.PASSWORD
        self.driver.get(LOGIN_URL)
        self.driver.find_element_by_id("username").send_keys(USER_ID)
        self.driver.find_element_by_id("btnNext").click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("passwd").send_keys(PASSWORD)
        self.driver.find_element_by_id("btnSubmit").click()

        #Download csv file
        for code in settings.CSV_RANGE:
            csv_url = "https://stocks.finance.yahoo.co.jp/stocks/history/?code={0}.T".format(code)
            self.driver.get(csv_url)
            self.driver.implicitly_wait(3)
            try:
                #指定したURLが存在しない場合はfor文の先頭に戻る
                self.driver.find_element_by_class_name("selectFinTitle")
                time.sleep(1)
                continue
            except NoSuchElementException:
                pass
            try:
                self.driver.find_element_by_css_selector('a.stocksCsvBtn').click()
            except NoSuchElementException:
                pass
            time.sleep(5)



