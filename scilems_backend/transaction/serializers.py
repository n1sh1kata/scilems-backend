from rest_framework import serializers
from .models import Transaction
from cart.models import Cart
from cart.serializers import CartSerializer


class TransactionSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True, read_only=True)  # Serialize carts for the response
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
        carts = validated_data.pop('carts')  # Extract carts from the request
        transaction = Transaction.objects.create(**validated_data)

        # Associate carts with the transaction
        transaction.carts.set(carts)

        return transaction

    def validate(self, data):
        carts = data.get('carts', [])
        user = self.context['request'].user

        # Ensure all carts belong to the user
        for cart in carts:
            if cart.user != user:
                raise serializers.ValidationError("You can only include your own cart items in a transaction.")

        return data