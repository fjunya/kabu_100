from rest_framework import viewsets, filters
import django_filters
from app.models import ProfitAndLoss
from app.serializer import ProfitAndLossSerializer

class ProfitAndLossViewSet(viewsets.ModelViewSet):
    queryset = ProfitAndLoss.objects.all()
    serializer_class = ProfitAndLossSerializer