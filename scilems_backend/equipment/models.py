from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_no_category(sender, **kwargs):
    if sender.name == "equipment":
        Category.objects.get_or_create(categoryname="No Category")

class Category(models.Model):
    categoryname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.categoryname

    @staticmethod
    def get_default_category():
        category, created = Category.objects.get_or_create(categoryname="No Category")
        return category.id

class Equipment(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=Category.get_default_category,
        related_name="equipments"
    )
    eqname = models.CharField(max_length=255)
    imglink = models.URLField(blank=True, null=True)
    ytlink = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.eqname