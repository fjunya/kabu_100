from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import RawPrices
import csv
import glob
import os
import datetime
from django.db import IntegrityError

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
                    open_price=float(row[1]),
                    close_price=float(row[4]),
                    high_price=float(row[2]),
                    low_price=float(row[3]),
                    volume=int(row[5]),
                    adjustment_close_price=int(row[6])
                )
                try:
                    raw_prices.save()
                except IntegrityError as e:
                    print(e)
