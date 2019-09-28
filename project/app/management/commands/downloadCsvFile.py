from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from django.conf import settings

DRIVER_PATH = "./tmp/driver/geckodriver"
SECURITIES_CODE_LIST_PATH = "./tmp/securitiesCodeList/securitiesCodeList.txt"

class Command(BaseCommand):
    help = ''
    driver = webdriver.Firefox(executable_path=DRIVER_PATH)

    def handle(self, *args, **options):
        self.download()

    def yahooLogin(self):
        self.driver.get(settings.YAHOO_LOGIN_URL)
        self.driver.find_element_by_id("username").send_keys(settings.YAHOO_USER_ID)
        self.driver.find_element_by_id("btnNext").click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("passwd").send_keys(settings.YAHOO_PASSWORD)
        self.driver.find_element_by_id("btnSubmit").click()

    def download(self):
        """
        東証の銘柄をダウンロードする
        :return:
        """
        self.yahooLogin()

        with open(SECURITIES_CODE_LIST_PATH, "r") as code_list:
            for code in code_list:
                """
                証券コードの後に市場略称を付与する。東証のみのダウンロードなのでTを付与。
                https://www.yahoo-help.jp/app/answers/detail/p/546/a_id/45387
                """
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



