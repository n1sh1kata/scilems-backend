from django.db import models
from django.conf import settings
from equipment.models import Equipment

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.equipment.eqname} ({self.quantity})"