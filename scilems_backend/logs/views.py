from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TransactionLog
from .serializers import TransactionLogSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class TransactionLogListView(generics.ListAPIView):
    serializer_class = TransactionLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['transaction_id', 'user__username', 'log_type', 'message']
    ordering_fields = ['timestamp', 'transaction_id']
    ordering = ['-timestamp']

    def get_queryset(self):
        queryset = TransactionLog.objects.all()
        
        # Filter by transaction_id if provided
        transaction_id = self.request.query_params.get('transaction_id', None)
        if transaction_id is not None:
            queryset = queryset.filter(transaction_id=transaction_id)
            
        # Filter by log_type if provided
        log_type = self.request.query_params.get('log_type', None)
        if log_type is not None:
            queryset = queryset.filter(log_type=log_type)

        return queryset