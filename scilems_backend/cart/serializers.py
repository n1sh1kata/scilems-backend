from rest_framework import serializers
from .models import Cart
from equipment.models import Equipment

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'equipment', 'quantity']
        read_only_fields = ['user']

    def validate_quantity(self, value):
        # Ensure the equipment field is an ID, not an object
        equipment_id = self.instance.equipment.id if self.instance else self.initial_data.get('equipment')
        try:
            equipment_obj = Equipment.objects.get(id=equipment_id)
        except Equipment.DoesNotExist:
            raise serializers.ValidationError("The specified equipment does not exist.")

        if value <= 0 or value > equipment_obj.stock:
            raise serializers.ValidationError(f"Quantity must be greater than 0 and less than or equal to the stock ({equipment_obj.stock}).")
        return value

    def update(self, instance, validated_data):
        # Prevent updating the equipment field
        validated_data.pop('equipment', None)
        return super().update(instance, validated_data)