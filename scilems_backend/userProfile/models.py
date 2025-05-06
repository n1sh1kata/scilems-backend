from django.db import models
from django.conf import settings
from PIL import Image
from django.core.exceptions import ValidationError

# Define the validate_image function
def validate_image(image):
    if image.size > 2 * 1024 * 1024:  # 2MB limit
        raise ValidationError("Image file size must not exceed 2MB.")
    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raise ValidationError("Only JPEG, PNG, and WebP file types are allowed.")

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True, validators=[validate_image])
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            # Crop to 1:1 aspect ratio
            width, height = img.size
            min_dim = min(width, height)
            img = img.crop((0, 0, min_dim, min_dim))
            # Resize if necessary
            img.thumbnail((500, 500))
            img.save(self.image.path)

    def __str__(self):
        return f"{self.firstname} {self.lastname}'s Profile"
    

import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# Signal to delete the image file when the UserProfile is deleted
@receiver(post_delete, sender=UserProfile)
def delete_image_on_profile_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# Signal to delete the old image file when the UserProfile image is updated
@receiver(pre_save, sender=UserProfile)
def delete_old_image_on_profile_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if the instance is new

    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return

    # Check if the image is being updated
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)