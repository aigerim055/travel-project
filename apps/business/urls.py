from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    GuideViewSet, 
    BusinessView, 
    BusinessRetrieveView, 
    BusinessDeleteView 
)



router = DefaultRouter()
router.register('guide', GuideViewSet, 'guide')




urlpatterns = [ 
    path('business/', BusinessView.as_view(), name='creation'),
    path('business/<str:slug>', BusinessView.as_view(), name='creation'),
    path('business/<str:slug>/', BusinessRetrieveView.as_view(), name='get_business'),
    path('business/delete/<str:slug>/', BusinessDeleteView.as_view(), name='get_business'),
]
urlpatterns += router.urls