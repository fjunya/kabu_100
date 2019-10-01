from django.core.management.base import BaseCommand
from app.models import RawPrices
import pandas as pd
import matplotlib.pyplot as plt
import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('code', type=int, help="証券コードを指定してください")
        parser.add_argument('start_date', type=str, help="yyyy-mm形式で指定してください")

    def handle(self, *args, **options):
        self.view_stock_chart(options['code'], options['start_date'])

    def view_stock_chart(self, code, start_date_str):
        rolling_day = 75
        start_date = datetime.datetime.strptime(start_date_str + "-01", "%Y-%m-%d")
        # 75日移動平均線を求める為に余分にデータを取得。土日を考慮して110日より前から取得
        rawPrices = RawPrices.objects\
            .filter(code=code)\
            .filter(date__gt=start_date - datetime.timedelta(days=110))\
            .order_by('date')
        rawPriceList = list(map(lambda x: [x.date, x.open_price, x.close_price], rawPrices))
        columns = ["date", "open_price", "close_price"]
        df = pd.DataFrame(rawPriceList, columns=columns)
        df.date = pd.to_datetime(df.date)
        df.set_index("date", inplace=True)
        df.loc[start_date_str:, ['open_price', 'close_price']].plot()
        # 移動平均線を求める為に、全てのデータから計算(表示する期間だけで計算すると最初の方の移動平均線を求められない為)
        roll_mean = df.close_price.rolling(window=rolling_day).mean()
        # 移動平均線を表示
        roll_mean.loc[start_date_str:].plot()
        plt.xlabel('Date')
        plt.ylabel('Stock price')
        plt.show()

