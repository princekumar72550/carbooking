from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False)
    profile_photo = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone', 'gender', 'profile_photo']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        # Extract profile-related data
        phone = validated_data.pop('phone', '')
        gender = validated_data.pop('gender', '')
        profile_photo = validated_data.pop('profile_photo', None)
        
        # Remove password_confirm and password from validated_data
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create username from email (before @ symbol)
        email = validated_data.get('email')
        username = email.split('@')[0]
        validated_data['username'] = username
        
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create or update user profile
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if phone:
            user_profile.phone = phone
        if gender:
            user_profile.gender = gender
        if profile_photo:
            user_profile.profile_picture = profile_photo
        user_profile.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        return data