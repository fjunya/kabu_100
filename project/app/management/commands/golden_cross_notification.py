from django.core.management.base import BaseCommand
from app.models import RawPrices, Company
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.notification()

    def notification(self):
        companies = Company.objects.all()
        notification_list = []
        for company in companies:
            raw_prices = RawPrices.objects.filter(code=company.code).order_by("-date")[:2]
            series1 = pd.DataFrame(list(map(lambda x: [x.date, x.moving_averages5], raw_prices)),
                                   columns=["date", "sma"])
            series1.set_index("date", inplace=True)
            series2 = pd.DataFrame(list(map(lambda x: [x.date, x.moving_averages25], raw_prices)),
                                   columns=["date", "sma"])
            series2.set_index("date", inplace=True)
            if self.crossover(series1, series2):
                notification_list.append(company)
        if len(notification_list) > 0:
            self.send_mail(notification_list)

    def crossover(self, series1: pd.Series, series2: pd.Series) -> bool:
        """
        series1がseries2をしたから上に突き抜けたらTrueを返す
        :param series1:
        :param series2:
        :return:
        """
        if(series1.size < 2):
            return False
        try:
            return series1.sma[1] < series2.sma[1] and series1.sma[0] > series2.sma[0]
        except IndexError:
            return False

    def send_mail(self, company_list):
        message = ""
        for company in company_list:
            text = "証券コード : {}\n".format(company.code)
            message+=text
        subject = "ゴールデンクロス情報"
        from_email = settings.FROM_EMAIL  # 送信者
        recipient_list = settings.RECIPIENT_LIST  # 宛先リスト
        send_mail(subject, message, from_email, recipient_list)