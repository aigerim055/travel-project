from django.urls import path

from .views import (
    TourView,
    TourRetrieveUpdateDeleteView,
    ConcreteTourView,
    ConcreteTourDeleteUpdateView,
)


urlpatterns = [ 

    path('concrete-tour/<str:slug>/', ConcreteTourDeleteUpdateView.as_view(), name='concrete-tour'),
    path('tour/<str:slug>/', TourRetrieveUpdateDeleteView.as_view(), name='tour-retrieve'),
    path('tour/', TourView.as_view(), name='tour'),
    path('concrete-tour/', ConcreteTourView.as_view(), name='consrete-tour'),
    path('concrete-tour/<str:slug>/', ConcreteTourView.as_view(), name='concrete-tour'),

]
