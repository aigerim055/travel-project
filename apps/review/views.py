from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)

from crypt import methods
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import(
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework import mixins

from apps.business.permissions import IsOwner
from apps.tour.models import Tour

from .serializers import (
    RatingSerializer,
    CommentSerializer,
    FavoriteSerializer,
    GuideRatingSerializer,
    LikeSerializer,
)
from .models import (
    TourComment, 
    TourFavorite, 
    TourRating,
    GuideRating,
)


class FavoriteViewSet(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = FavoriteSerializer
    queryset = TourFavorite.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'favorite' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'favorite' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def favorite(self, request, pk=None):
        tour = self.get_object().get('slug')
        serializer = FavoriteSerializer(
            data=request.data, 
            context={
                'request':request,
                'tour':tour
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Successfully added to favorites!')
            if request.method == 'DELETE':
                        serializer.del_favorite()
                        return Response('Successfully removed from favorites!')


class CommentView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = TourComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RatingView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = TourRating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class GuideRatingView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = GuideRating.objects.all()
    serializer_class = GuideRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikeView(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = FavoriteSerializer
    queryset = TourFavorite.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'like' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'like' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def like(self, request, pk=None):
        post = self.get_object()
        serializer = LikeSerializer(
            data=request.data, 
            context={
                'request':request,
                'post':post
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('unliked!')
