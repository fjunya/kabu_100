from django.core.management.base import BaseCommand
from app.models import RawPrices, Company
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
import logging
logger = logging.getLogger(__name__)


SURVEY_DATE = "2019-01-01"

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.backtest()

    def backtest(self):
        company = Company.objects.filter(code=4776).first()
        df = self.get_data(company.code)
        bt = Backtest(df, SmaCross, cash=10000)
        print(bt.run())
        bt.plot()

    def get_data(self, code):
        raw_prices = RawPrices.objects.filter(code=code)
        raw_prices = raw_prices.filter(date__gte=SURVEY_DATE)
        raw_prices = raw_prices.exclude(moving_averages75=-1).order_by("date")
        raw_price_list = list(
            map(lambda x: [x.date, x.open_price, x.high_price, x.low_price, x.close_price, x.moving_averages25, x.moving_averages75], raw_prices))
        columns = ["date", "Open", "High", "Low", "Close", "sma25", "sma75"]
        df = pd.DataFrame(raw_price_list, columns=columns)
        df.date = pd.to_datetime(df.date)
        df.set_index("date", inplace=True)
        return df

class SmaCross(Strategy):

    def init(self):
        """
        sma1に25日平均線のデータをセット
        sma2に75日平均線のデータをセット
        :return:
        """
        self.sma1 = self.I(sma, self.data.sma25) #Iの引数に関数と関数の引数を渡す
        self.sma2 = self.I(sma, self.data.sma75)

    def next(self):
        """
        ゴールデンクロスの時に買い、デッドクロスの時に売却する
        :return:
        """
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()

def sma(data: pd.Series):
    return data