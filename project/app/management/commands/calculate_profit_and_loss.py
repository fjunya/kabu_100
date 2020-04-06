from django.core.management.base import BaseCommand
from app.models import InvestmentRecord, ProfitAndLoss, ProfitAndLossInvestmentRecordMap
from app.enum.buy_sell_classification import BuySellClassification
import dataclasses

import logging

logger = logging.getLogger(__name__)

@dataclasses.dataclass
class BuyInvestmentRecordElement:
    investment_record: InvestmentRecord
    amount: int


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.calculate_investment_records()
        # self.delete_all()

    def delete_all(self):
        ProfitAndLoss.objects.all().delete()
        InvestmentRecord.objects.all().delete()
        ProfitAndLossInvestmentRecordMap.objects.all().delete()

    def calculate_investment_records(self):
        sell_investment_records = InvestmentRecord.objects.filter(is_profit_and_loss=False).filter(
            buy_sell_classification=BuySellClassification.SELL.value)
        for investment_record in sell_investment_records:
            self.calculate_investment_record(investment_record)

    def calculate_investment_record(self, sell_investment_record: InvestmentRecord,
                                    profit_and_loss: ProfitAndLoss = None):
        if not profit_and_loss:
            profit_and_loss = ProfitAndLoss(
                code=sell_investment_record.code,
                profit_and_loss=0,
                average_buy_price=0,
                average_sell_price=0,
                sell_investment_record=sell_investment_record
            )
        buy_investment_records = InvestmentRecord.objects.filter(amount_remaining__gt=0).filter(
            buy_sell_classification=BuySellClassification.BUY.value).filter(code=sell_investment_record.code)
        total_amount = 0
        sell_amount = profit_and_loss.sell_investment_record.amount
        is_calculate = False
        buy_investment_record_element_list = []
        for buy_record in buy_investment_records:
            if sell_amount <= total_amount + buy_record.amount_remaining:
                buy_record.amount_remaining = (total_amount + buy_record.amount_remaining) - sell_amount
                buy_investment_record_element_list.append(
                    BuyInvestmentRecordElement(buy_record,  sell_amount - total_amount))
                is_calculate = True
                break
            total_amount += buy_record.amount_remaining
            buy_investment_record_element_list.append(
                BuyInvestmentRecordElement(buy_record, buy_record.amount_remaining))
            buy_record.amount_remaining = 0
        if not is_calculate:
            return
        buy_price = 0
        sell_price = sell_investment_record.amount * sell_investment_record.price
        for buy_investment_record_element in buy_investment_record_element_list:
            buy_price += buy_investment_record_element.investment_record.price * buy_investment_record_element.amount
        profit_and_loss.profit_and_loss = sell_price - buy_price
        profit_and_loss.average_buy_price = buy_price / sell_investment_record.amount
        profit_and_loss.average_sell_price = sell_investment_record.price
        try:
            profit_and_loss.save()
            sell_investment_record.is_profit_and_loss = True
            sell_investment_record.save()
            for buy_investment_record_element in buy_investment_record_element_list:
                buy_investment_record_element.investment_record.save()
                profitAndLoss_investment_record_map = ProfitAndLossInvestmentRecordMap(
                    profit_and_loss=profit_and_loss,
                    investment_record=buy_investment_record_element.investment_record,
                    amount=buy_investment_record_element.amount
                )
                profitAndLoss_investment_record_map.save()
        except Exception as e:
            logger.exception(e)
