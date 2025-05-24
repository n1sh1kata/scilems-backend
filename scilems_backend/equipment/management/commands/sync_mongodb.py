from django.core.management.base import BaseCommand
from equipment.mongo.sync import sync_to_mongodb

class Command(BaseCommand):
    help = 'Synchronizes Equipment and Category data to MongoDB'

    def handle(self, *args, **options):
        success, message = sync_to_mongodb()
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))