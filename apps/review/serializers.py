from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    TourComment,
    TourFavorite,
    TourRating,
    GuideRating,
    TourLike,
)


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = TourComment
        exclude = ['id']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = TourRating
        fields = ('rating', 'user', 'tour')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('Неправлильное значение. Рейтинг должен быть между 1 и 5.')
        if rating:
            raise serializers.ValidationError('already exsits')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TourFavorite
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        tour = request.get('tour')
        favorite = TourFavorite.objects.filter(user=user, tour=tour).first()
        if not favorite:
            return super().create(validated_data)
        raise serializers.ValidationError('This tour has been added to favorites')

    def del_favorite(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        tour = request.get('tour').slug
        favorite = TourFavorite.objects.filter(user=user, tour=tour).first()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('This tour is not in favorites')


class GuideRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = GuideRating
        fields = ('rating', 'user', 'guide', 'id')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('wrong value! rating must be between 1 and 5')
        if rating:
            raise serializers.ValidationError('already exsits')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    

    class Meta:
        model = TourLike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        tour = self.context.get('tour')
        like = TourLike.objects.filter(user=user, tour=tour).first()
        if like:
            raise serializers.ValidationError('already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        tour = self.context.get('tour')
        like = TourLike.objects.filter(user=user, tour=tour).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('not liked yet')