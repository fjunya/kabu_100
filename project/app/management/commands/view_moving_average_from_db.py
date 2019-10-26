from django.core.management.base import BaseCommand
from app.models import RawPrices
import pandas as pd
import matplotlib.pyplot as plt

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('code', type=int, help="証券コードを指定してください")
        parser.add_argument('start_date', type=str, help="yyyy-mm形式で指定してください")

    def handle(self, *args, **options):
        self.view_stock_chart(options['code'], options['start_date'])

    def view_stock_chart(self, code, start_date):
        raw_prices = RawPrices.objects\
            .filter(code=code)\
            .filter(date__gt=start_date + "-01")\
            .order_by('date')
        raw_price_list = list(map(lambda x: [x.date, x.adjustment_close_price, x.moving_averages5, x.moving_averages25, x.moving_averages75], raw_prices))
        columns = ["date", "adjustment_close_price", "moving_averages5", "moving_averages25", "moving_averages75"]
        df = pd.DataFrame(raw_price_list, columns=columns)
        df.date = pd.to_datetime(df.date)
        df.set_index("date", inplace=True)
        df.plot()
        plt.xlabel('Date')
        plt.ylabel('Stock price')
        plt.show()

