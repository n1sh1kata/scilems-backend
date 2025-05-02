from rest_framework import serializers
from .models import Transaction
from cart.models import Cart  # Ensure this import is present
from cart.serializers import CartSerializer

class TransactionSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True, read_only=True)
    cart_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Cart.objects.all(), write_only=True, source='carts'
    )

    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'carts', 'cart_ids', 'current_status', 'date_applied', 'date_approved',
            'pick_up_date', 'date_borrowed', 'return_date', 'date_returned', 'date_archived', 'remarks'
        ]
        read_only_fields = ['user', 'date_applied']

    def create(self, validated_data):
        carts = validated_data.pop('carts')
        transaction = Transaction.objects.create(**validated_data)
        transaction.carts.set(carts)
        return transaction

    def update(self, instance, validated_data):
        carts = validated_data.pop('carts', None)
        if carts is not None:
            instance.carts.set(carts)
        return super().update(instance, validated_data)