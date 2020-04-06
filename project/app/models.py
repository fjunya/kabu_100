from django.db import models

class Company(models.Model):
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)

    def __str__(self):
        return self.name

class RawPrices(models.Model):
    code = models.IntegerField("銘柄コード")
    date = models.DateField("日付")
    open_price = models.IntegerField("始値")
    close_price = models.IntegerField("終値")
    high_price = models.IntegerField("高値")
    low_price = models.IntegerField("安値")
    volume = models.IntegerField("出来高")
    adjustment_close_price = models.FloatField("調整後終値")
    moving_averages5 = models.FloatField("5日移動平均線", null=True)
    moving_averages25 = models.FloatField("25日移動平均線", null=True)
    moving_averages75 = models.FloatField("75日移動平均線", null=True)
    is_moving_average = models.BooleanField("移動平均線算出済み")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'date'], name='unique_code_dete'),
        ]

class InvestmentRecord(models.Model):
    contract_date = models.DateField("約定日")
    code = models.IntegerField("銘柄コード")
    amount = models.IntegerField("数量")
    amount_remaining = models.IntegerField("損益計算の残り数量")
    price = models.FloatField("単価")
    commission = models.IntegerField("手数料(円)")
    tax = models.IntegerField("税金等")
    total_price = models.IntegerField("受渡金額")
    buy_sell_classification = models.IntegerField("売買区分")
    is_short = models.BooleanField("空売りか否か")
    is_profit_and_loss = models.BooleanField("損出に紐付け済み")

    def __str__(self):
        return str(self.id)

class ProfitAndLoss(models.Model):
    code = models.IntegerField("銘柄コード")
    profit_and_loss = models.IntegerField("損益")
    average_buy_price = models.FloatField("平均購入単価")
    average_sell_price = models.FloatField("平均売却単価")
    # buy_investment_records = models.ManyToManyField(InvestmentRecord, blank=True)
    sell_investment_record = models.OneToOneField(InvestmentRecord, on_delete=models.CASCADE, blank=True, related_name="sell_investment_records")

class ProfitAndLossInvestmentRecordMap(models.Model):
    profit_and_loss = models.ForeignKey(ProfitAndLoss, on_delete=models.CASCADE)
    investment_record = models.ForeignKey(InvestmentRecord, on_delete=models.CASCADE)
    amount = models.IntegerField("数量")





