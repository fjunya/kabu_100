from django.core.management.base import BaseCommand
from app.models import RawPrices, Company
import pandas as pd
import numpy as np

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.save_moving_averages()

    def save_moving_averages(self):
        companies = Company.objects.all()
        for company in companies:
            self.save_moving_average(company.code)

    def save_moving_average(self, code):
        raw_prices = RawPrices.objects.filter(code=code).order_by('date')
        raw_price_list = list(map(lambda x: [x.date, x.adjustment_close_price], raw_prices))
        columns = ["date", "adjustment_close_price"]
        df = pd.DataFrame(raw_price_list, columns=columns)
        df.date = pd.to_datetime(df.date)
        df.set_index("date", inplace=True)
        moving_averages25 = df.rolling(window=25).mean()
        moving_averages25.rename(columns={'adjustment_close_price': '25_moving_averages'}, inplace=True)
        moving_averages75 = df.rolling(window=75).mean()
        moving_averages75.rename(columns={'adjustment_close_price': '75_moving_averages'}, inplace=True)
        data = pd.concat([df, moving_averages25, moving_averages75], axis=1)
        for raw_price in raw_prices:
            if raw_price.moving_averages25 > 0 or raw_price.moving_averages25 == -1:
                next()
            raw_price.moving_averages25 = -1 if np.isnan(data.loc[raw_price.date]['25_moving_averages']) else \
                data.loc[raw_price.date]['25_moving_averages']
            raw_price.moving_averages75 = -1 if np.isnan(data.loc[raw_price.date]['75_moving_averages']) else \
                data.loc[raw_price.date]['75_moving_averages']
            raw_price.save()


