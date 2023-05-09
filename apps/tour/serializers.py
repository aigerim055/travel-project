from rest_framework import serializers
from django.db.models import Avg
from apps.review.serializers import CommentSerializer, LikeSerializer
from django.contrib.auth import get_user_model

from .models import Tour, TourImage, ConcreteTour


User = get_user_model()

class TourCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tour
        fields = '__all__'

    tour_image_carousel = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
    )

    def create(self, validated_data):
        image_carousel = validated_data.pop('tour_image_carousel')
        tour = Tour.objects.create(**validated_data)
        images = []
        for image in image_carousel:
            images.append(TourImage(tour=tour, image=image))
        TourImage.objects.bulk_create(images)
        tour.save()
        user = self.context['request'].user
        return tour

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data

    
class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['carousel'] = TourImageSerializer(
            instance.tour_images.all(), many=True
        ).data
        return representation


class TourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'image', 'place', 'level', 'number_of_days', 'company_name']


class ConcreteTourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcreteTour
        fields = '__all__'

    def create(self, validated_data):
        tour = ConcreteTour.objects.create(**validated_data)
        return tour

    


class ConcreteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcreteTour
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rating'] = RatingSerializer(
        #     instance.rating_tour.all(),
        #     many=True
        # ).data
        rating = instance.rating_tour.aggregate(Avg('rating'))['rating__avg']
        rep['comments'] = CommentSerializer(
            instance.comment_tour.all(),
            many=True
        ).data
        rep['likes'] = instance.like_tour.all().count()
        rep['liked_by'] = LikeSerializer(instance.like_tour.all().only('user'), many=True).data
        if rating:
            rep['rating'] = round(rating,1)
        else:
            rep['rating'] = 0.0
        return rep

class ConcreteTourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcreteTour
        fields = '__all__'

    
class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = 'image',