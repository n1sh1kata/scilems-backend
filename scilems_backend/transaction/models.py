from django.db import models
from django.conf import settings
from cart.models import Cart

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('applying', 'Applying'),
        ('approved', 'Approved'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    carts = models.ManyToManyField(Cart, related_name="transactions")
    current_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='applying')
    date_applied = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    pick_up_date = models.DateTimeField(null=True, blank=True)
    date_borrowed = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    date_archived = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username}"