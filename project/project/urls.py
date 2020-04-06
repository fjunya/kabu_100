from django.contrib import admin
from django.urls import path, include
from app.urls import router as app_api_router

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(app_api_router.urls)),
]
