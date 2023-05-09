from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import mixins

from .models import TourPurchase
from .serializers import (

    TourPurchaseSerializer,
    PurchaseHistorySerializer,
)


class OrderViewSet(mixins.CreateModelMixin,
    GenericViewSet):
    
    serializer_class = TourPurchaseSerializer
    permission_classes = [IsAuthenticated]   

    def get_queryset(self):
        user = self.request.user
        return TourPurchase.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrderHistoryView(ListAPIView):
   
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TourPurchase.objects.filter(user=user)