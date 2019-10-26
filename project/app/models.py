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