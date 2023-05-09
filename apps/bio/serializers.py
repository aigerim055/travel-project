from rest_framework import serializers, status
from django.contrib.auth import get_user_model

from .models import UserProfile
from apps.business.models import BusinessProfile



User = get_user_model()


class UserProfileCreateSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=40)
    birthday = serializers.DateField()

    def create(self, validated_data):
        profile = UserProfile.objects.create(**validated_data)
        return profile

    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        business = BusinessProfile.objects.filter(user=user).first()
        if business:
                raise serializers.ValidationError('У вас уже существует бизнес профиль!')
        return attrs

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserProfile
