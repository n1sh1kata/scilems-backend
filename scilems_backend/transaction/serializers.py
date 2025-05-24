from .models import Transaction, TransactionItem
from cart.models import Cart
from cart.serializers import CartSerializer
from rest_framework import serializers

class TransactionItemSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.eqname', read_only=True)

    class Meta:
        model = TransactionItem
        fields = ['id', 'equipment', 'equipment_name', 'quantity']

class TransactionSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True, read_only=True)
    cart_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Cart.objects.all(), write_only=True, source='carts'
    )
    items = TransactionItemSerializer(many=True, read_only=True)  # <-- Add this line

    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'carts', 'cart_ids', 'items', 'current_status', 'date_applied', 'date_approved',
            'pick_up_date', 'date_borrowed', 'return_date', 'date_returned', 'date_archived', 'remarks'
        ]
        read_only_fields = ['user', 'date_applied']

    def create(self, validated_data):
        carts = validated_data.pop('carts')
        transaction = Transaction.objects.create(**validated_data)
        transaction.carts.set(carts)
        return transaction

    def validate(self, data):
        carts = data.get('carts', [])
        user = self.context['request'].user
        for cart in carts:
            if cart.user != user:
                raise serializers.ValidationError("You can only include your own cart items in a transaction.")
        return data