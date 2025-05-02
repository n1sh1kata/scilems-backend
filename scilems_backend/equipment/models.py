from django.db import models

class Category(models.Model):
    categoryname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.categoryname


class Equipment(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="equipments")
    eqname = models.CharField(max_length=255)
    imglink = models.URLField(blank=True, null=True)
    ytlink = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.eqname