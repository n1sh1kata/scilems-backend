from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from scilems_backend.utils import rate_limit
from .models import Transaction
from rest_framework import status
from .serializers import TransactionSerializer

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins to perform all actions.
    - Regular users to only view their own transactions and create new ones.
    """

    def has_permission(self, request, view):
        # Admins can perform all actions
        if request.user.is_authenticated and request.user.role == 'admin':
            return True

        # Regular users can only perform safe methods (GET, HEAD, OPTIONS) or create transactions (POST)
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Admins can perform all actions
        if request.user.role == 'admin':
            return True

        # Regular users can only view their own transactions
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        # Deny update or delete for regular users
        return False


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Regular users can only see their own transactions
        if self.request.user.role != 'admin':
            return Transaction.objects.filter(user=self.request.user)
        return Transaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @rate_limit(requests=5, window=300)  # 5 transactions per 5 minutes
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admins can access all transactions
        if self.request.user.role == 'admin':
            return Transaction.objects.all()

        # Regular users can only access their own transactions
        return Transaction.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Transaction deleted successfully."}, status=status.HTTP_200_OK)