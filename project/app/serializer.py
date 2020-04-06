from rest_framework import serializers
from app.models import ProfitAndLoss


class ProfitAndLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitAndLoss
        fields = ('code', 'profit_and_loss')