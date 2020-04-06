from rest_framework import routers
from app.views import ProfitAndLossViewSet

router = routers.DefaultRouter()
router.register(r'profit_and_loss', ProfitAndLossViewSet)