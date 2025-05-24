from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from scilems_backend.utils import rate_limit
from .models import Transaction, TransactionItem
from .serializers import TransactionSerializer
from cart.models import Cart
from equipment.models import Equipment
from logs.models import TransactionLog

class IsAdminOrCreateOnly(permissions.BasePermission):
    """
    - Allow create for any authenticated user.
    - Allow read/update/delete for admin only.
    """
    def has_permission(self, request, view):
        if view.action == 'create' or (hasattr(view, 'action') and view.action == 'create'):
            return request.user.is_authenticated
        # Only admin for other actions
        return request.user.is_authenticated and request.user.role == 'admin'

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Create allowed for all authenticated

    def get_queryset(self):
        # Only admin can list all, users see only their own
        if self.request.user.role == 'admin':
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        # Create creation log
        TransactionLog.objects.create(
            transaction_id=transaction.id,
            user=self.request.user,
            log_type='creation',
            new_status='applying',
            message=f'Transaction created by {self.request.user.username}',
            details={'cart_items': list(transaction.carts.values('equipment__eqname', 'quantity'))}
        )

    @rate_limit(requests=5, window=300)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        # Only admin can access
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admin can access this resource.")
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_status = instance.current_status
        response = super().update(request, *args, **kwargs)
        instance.refresh_from_db()

        # Log status change
        if prev_status != instance.current_status:
            TransactionLog.objects.create(
                transaction_id=instance.id,
                user=self.request.user,
                log_type='status_change',
                previous_status=prev_status,
                new_status=instance.current_status,
                message=f'Status changed from {prev_status} to {instance.current_status} by {self.request.user.username}',
                details={
                    'items': list(instance.items.values('equipment__eqname', 'quantity')),
                    'remarks': instance.remarks
                }
            )

            if instance.current_status == 'approved':
                # Move carts to TransactionItem and deduct stock
                for cart in instance.carts.all():
                    TransactionItem.objects.create(
                        transaction=instance,
                        equipment=cart.equipment,
                        quantity=cart.quantity
                    )
                    cart.equipment.stock = max(cart.equipment.stock - cart.quantity, 0)
                    cart.equipment.save()
                    cart.delete()
            elif instance.current_status == 'returned':
                # Add stock back using TransactionItems
                for item in instance.items.all():
                    equipment = item.equipment
                    equipment.stock += item.quantity
                    equipment.save()
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Log deletion
        TransactionLog.objects.create(
            transaction_id=instance.id,
            user=request.user,
            log_type='deletion',
            previous_status=instance.current_status,
            message=f'Transaction deleted by {request.user.username}',
            details={'last_status': instance.current_status}
        )
        return super().destroy(request, *args, **kwargs)