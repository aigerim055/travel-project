from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from django.http import Http404
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .permissions import IsOwner
from .models import BusinessProfile, Guide
from .serializers import (
    BusinessProfileCreateSerializer,
    BusinessProfileListSerializer,
    BusinessProfileSerializer,
    GuideListSerializer,
    GuideSerializer,
)


class BusinessView(APIView):
    search_fields = ['title']

    def get(self, request: Request):
        bus = BusinessProfile.objects.all()
        serializer = BusinessProfileListSerializer(bus, many=True)

        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BusinessProfileCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(
                'Вы успешно создали бизнес-профиль', 
                status=status.HTTP_201_CREATED
            )

    def get_object(self, slug):
        try:
            return BusinessProfile.objects.get(slug=slug)
        except BusinessProfile.DoesNotExist:
            raise Http404


class BusinessRetrieveView(APIView):
    @method_decorator(cache_page(60*5))
    @method_decorator(vary_on_cookie)
    def get(self, request, slug):
        try:
            bus = BusinessProfile.objects.filter(slug=slug)
            serializer = BusinessProfileSerializer(bus).data
            return Response(serializer)
        except BusinessProfile.DoesNotExist:
            raise Http404


class BusinessDeleteView(APIView):
    permission_classes = [IsOwner]
    def delete(self, request: Request, slug):
        profile = BusinessProfile.objects.get(slug=slug)
        profile.delete()
        return Response(
            'Ваш бизнес профиль удален.',
            status=status.HTTP_204_NO_CONTENT
        )


class GuideViewSet(ModelViewSet):      
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GuideListSerializer
        elif self.action == 'create':
            return GuideSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            self.permission_classes = [IsOwner]
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [AllowAny] 
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context