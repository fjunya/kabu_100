from django.db import models

class Company(models.Model):
    code = models.IntegerField("銘柄コード", primary_key=True)
    name = models.CharField("会社名", max_length=200)