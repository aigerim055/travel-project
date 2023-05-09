from email.policy import default
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.account.utils import normalize_phone
from .models import (
    BusinessProfile,
    Guide,
    BusinessImage
)


User = get_user_model()


class BusinessProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BusinessProfile
        fields = '__all__'

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format!')
        return phone  

    def create(self, validated_data):
        profile = BusinessProfile.objects.create(**validated_data)
        return profile
     

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = 'image',


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BusinessProfile
        fields = '__all__'

    def to_representation(self, instance):         
        rep =  super().to_representation(instance)
        rep['guides'] = GuideListSerializer(
            instance.comp.all(), many=True
        ).data
        return rep
        # rep['tour'] = TourListSerializer(
        #     instance.title.all(), many=True
        # ).data


class BusinessProfileListSerializer(serializers.ModelSerializer):

     class Meta:
        model = BusinessProfile
        fields = ['title', 'phone', 'email', 'address']


class GuideSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    company_name = serializers.ReadOnlyField(source='company_name.title')

    class Meta:
        model = Guide 
        fields = '__all__'

    def create(self, validated_data):
        guide = Guide.objects.create(**validated_data)
        return guide

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        attrs['company_name'] = user.profile
        return attrs


class GuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        exclude = ['slug', 'company_name']