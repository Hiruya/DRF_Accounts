import datetime
from rest_framework import serializers
from .models import UserProfile, MemberProfile

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        # Convert the date to YYYY/MM/DD format
        if value:
            return value.strftime('%Y/%m/%d')
        return ''

    def to_internal_value(self, data):
        # Convert the incoming string to a date object
        try:
            return datetime.strptime(data, '%Y/%m/%d').date()
        except ValueError:
            raise serializers.ValidationError('Date format should be YYYY/MM/DD')
        
class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False)  # Make this optional if you prefer
    phone_number = serializers.CharField(required=True)
    date_of_birth = CustomDateField(required=True)
    gender = serializers.ChoiceField(choices=MemberProfile.GENDER_CHOICES, required=True)
    height = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    medical_history = serializers.CharField(required=False)

class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = [
            'full_name', 'profile_picture', 'phone_number', 'date_of_birth',
            'gender', 'height', 'weight', 'medical_history'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    profile = MemberProfileSerializer()

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = UserProfile.objects.create_user(**validated_data)
        
        MemberProfile.objects.create(user=user, **profile_data)

        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
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
        fields = ['full_name', 'profile_picture', 'phone_number', 'date_of_birth', 'gender', 'height', 'weight', 'medical_history']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
