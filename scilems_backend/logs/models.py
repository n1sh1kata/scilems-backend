from django.db import models
from django.conf import settings

class TransactionLog(models.Model):
    LOG_TYPES = (
        ('status_change', 'Status Change'),
        ('creation', 'Creation'),
        ('deletion', 'Deletion'),
    )

    transaction_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    previous_status = models.CharField(max_length=20, null=True, blank=True)
    new_status = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    details = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.log_type} - {self.timestamp}"