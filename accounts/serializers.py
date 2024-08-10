from rest_framework import serializers
from .models import CustomUser, MemberProfile

class Register1Serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # To ensure password is not returned in responses
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class Register2Serializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['full_name', 'phone_number', 'date_of_birth', 'gender', 'height', 'weight', 'medical_history']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Optional password update
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['full_name', 'phone_number', 'date_of_birth', 'gender', 'height', 'weight', 'medical_history']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
