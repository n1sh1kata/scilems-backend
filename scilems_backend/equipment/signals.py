from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Equipment, Category
from .mongo.sync import sync_to_mongodb

@receiver([post_save, post_delete], sender=Equipment)
@receiver([post_save, post_delete], sender=Category)
def sync_to_mongo(sender, **kwargs):
    sync_to_mongodb()