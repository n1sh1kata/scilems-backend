from rest_framework import serializers
from .models import Cart
from equipment.models import Equipment

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'equipment', 'quantity']
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        equipment = attrs.get('equipment')

        # Check if the equipment is already in the user's cart
        if Cart.objects.filter(user=user, equipment=equipment, transaction__isnull=True).exists():
            raise serializers.ValidationError(
                f"The equipment '{equipment.eqname}' is already in your cart."
            )

        return attrs

    def validate_quantity(self, value):
        equipment_id = self.initial_data.get('equipment')
        try:
            equipment_obj = Equipment.objects.get(id=equipment_id)
        except Equipment.DoesNotExist:
            raise serializers.ValidationError("The equipment you selected does not exist. Please choose a valid item.")

        if value <= 0:
            raise serializers.ValidationError("The quantity must be greater than 0.")
        if value > equipment_obj.stock:
            raise serializers.ValidationError(
                f"Only {equipment_obj.stock} units of '{equipment_obj.eqname}' are available. Please adjust your quantity."
            )
        return value