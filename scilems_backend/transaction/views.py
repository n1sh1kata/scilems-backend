from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Transaction
from .serializers import TransactionSerializer

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow only admins to perform all actions.
    Regular users can only create transactions with status 'applying' and view their own transactions.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access all transactions
        if request.user.role == 'admin':
            return True

        # Regular users can only access their own transactions
        return obj.user == request.user


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Regular users can only see their own transactions
        if self.request.user.role != 'admin':
            return Transaction.objects.filter(user=self.request.user)
        return Transaction.objects.all()

    def perform_create(self, serializer):
        # Restrict regular users to only create transactions with status 'applying'
        if self.request.user.role != 'admin' and serializer.validated_data.get('current_status') != 'applying':
            raise PermissionDenied("You can only create transactions with status 'applying'.")
        serializer.save(user=self.request.user)


from rest_framework.response import Response
from rest_framework import status

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        # Regular users can only see their own transactions
        if self.request.user.role != 'admin':
            return Transaction.objects.filter(user=self.request.user)
        return Transaction.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Transaction deleted successfully."}, status=status.HTTP_200_OK)