from rest_framework import serializers
from .models import TransactionLog

class TransactionLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TransactionLog
        fields = ['id', 'transaction_id', 'username', 'log_type', 'previous_status', 
                 'new_status', 'timestamp', 'message', 'details']
        read_only_fields = fields