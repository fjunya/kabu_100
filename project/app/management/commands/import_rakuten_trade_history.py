from django.core.management.base import BaseCommand
from app.models import InvestmentRecord
from django.conf import settings
from app.enum.buy_sell_classification import BuySellClassification
import glob
import os
import pandas as pd
import datetime
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.import_csv_files()

    def import_csv_files(self):
        csv_dir = settings.RAKUTEN_TRADE_HISTORY_CSV_DIR
        for path in glob.glob(os.path.join(csv_dir, "*.csv")):
            self.import_csv_file(path)

    def import_csv_file(self, path):
        csv_file = pd.read_csv(path, encoding="cp932")
        for index,row in csv_file.iterrows():
            is_short = False #空売りの判別方法がわかったら実装
            if row["売買区分"] == "買付":
                buy_sell_classification = BuySellClassification.BUY.value
            elif row["売買区分"] == "売付":
                buy_sell_classification = BuySellClassification.SELL.value
            else:
                buy_sell_classification = BuySellClassification.OTHER.value
            investmentRecord = InvestmentRecord(
                contract_date=datetime.datetime.strptime(row[0], '%Y/%m/%d').date(),
                code=row["銘柄コード"],
                amount=int(row["数量［株］"].replace(",", "")),
                amount_remaining=int(row["数量［株］"].replace(",", "")),
                price=float(row["単価［円］"].replace(",", "")),
                commission=row["手数料［円］"],
                tax=row["税金等［円］"],
                total_price=int(row["受渡金額［円］"].replace(",", "")),
                buy_sell_classification=buy_sell_classification,
                is_short=is_short,
                is_profit_and_loss=False
            )
            try:
                investmentRecord.save()
            except Exception as e:
                logger.exception(e)


