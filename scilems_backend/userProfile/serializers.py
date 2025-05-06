from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'image', 'firstname', 'middlename', 'lastname', 'suffix', 'email']
        read_only_fields = ['user']

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError("Image file size must not exceed 2MB.")
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            raise serializers.ValidationError("Only JPEG, PNG, and WebP file types are allowed.")
        return value