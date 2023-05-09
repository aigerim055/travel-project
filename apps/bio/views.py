from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)

from .serializers import (
    UserProfileListSerializer,
    UserProfileSerializer,
    UserProfileCreateSerializer,
)
from apps.business.permissions import IsOwner
from .models import UserProfile


class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def check_businessprofile(self, request):
        serializer = UserProfileCreateSerializer(
                data=request.data, 
                context={
                    'request':request,
                })

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        elif self.action == 'retrieve':
            return UserProfileSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            self.permission_classes in [IsOwner, IsAdminUser]
        if self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()