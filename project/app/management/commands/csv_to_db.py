from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import RawPrices
import csv
import glob
import os
import datetime
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.generate_from_csv_dir()

    def generate_from_csv_dir(self):
        csv_dir = settings.CSV_DIR
        for path in glob.glob(os.path.join(csv_dir, "*.T.csv")):
            file_name = os.path.basename(path)
            code = file_name.split('.')[0]
            self.generate_price_from_csv_file(code, path)

    def generate_price_from_csv_file(self, code: str, csv_file_path):
        with open(csv_file_path, encoding="shift_jis") as f:
            reader = csv.reader(f)
            next(reader)  # 先頭行を飛ばす
            for row in reader:
                raw_prices = RawPrices(
                    code=code,
                    date=datetime.datetime.strptime(row[0], '%Y/%m/%d').date(),
                    open_price=int(row[1]),
                    close_price=int(row[4]),
                    high_price=int(row[2]),
                    low_price=int(row[3]),
                    volume=int(row[5]),
                    adjustment_close_price=float(row[6])
                )
                try:
                    raw_prices.save()
                except IntegrityError:
                    logger.info("(code={code}:{date})既に登録されております".format(code=code, date=raw_prices.date))
                    # 重複エラーが出た場合はfor文から抜ける
                    break
                except Exception as e:
                    logger.exception(e)
                    logger.error("(code={code}:{date})登録に失敗しました".format(code=code, date=raw_prices.date))
