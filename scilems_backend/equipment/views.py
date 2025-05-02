from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Category, Equipment
from .serializers import CategorySerializer, EquipmentSerializer
from rest_framework.response import Response
from rest_framework import status

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Equipment deleted successfully."}, status=status.HTTP_200_OK)