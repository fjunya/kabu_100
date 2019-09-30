from django.db import models

class Company(models.Model):
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)

    def __str__(self):
        return "{code} : {name}".format(code=self.code, name=self.name)

class RawPrices(models.Model):
    code = models.IntegerField("銘柄コード")
    date = models.DateField("日付")
    open_price = models.IntegerField("始値")
    close_price = models.IntegerField("終値")
    high_price = models.IntegerField("高値")
    low_price = models.IntegerField("安値")
    volume = models.IntegerField("出来高")
    adjustment_close_price = models.IntegerField("調整後終値")

    def __str__(self):
        return "{code} : {date}".format(code=self.code, date=self.date)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'date'], name='unique_code_dete'),
        ]