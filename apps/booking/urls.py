from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import OrderHistoryView, OrderViewSet


router = DefaultRouter()
router.register('order', OrderViewSet, 'orders')

urlpatterns = [
    path('history/', OrderHistoryView.as_view())
]

urlpatterns += router.urls