from rest_framework import serializers
from .models import UserProfile
import os

class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)  # <-- Add allow_null and required=False
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'image', 'firstname', 'middlename', 'lastname', 'suffix', 'email']
        read_only_fields = ['user']

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB limit
            self._delete_temp_file(value)
            raise serializers.ValidationError("Image file size must not exceed 2MB.")
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            self._delete_temp_file(value)
            raise serializers.ValidationError("Only JPEG, PNG, and WebP file types are allowed.")
        return value

    def _delete_temp_file(self, file):
        # Remove the file from the temporary upload location if it exists
        try:
            if hasattr(file, 'temporary_file_path'):
                path = file.temporary_file_path()
                if os.path.exists(path):
                    os.remove(path)
            elif hasattr(file, 'path'):
                if os.path.exists(file.path):
                    os.remove(file.path)
        except Exception:
            pass

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except serializers.ValidationError as exc:
            image = self.initial_data.get('image')
            if image:
                self._delete_temp_file(image)
            raise