from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.filters import SearchFilter, OrderingFilter

from scilems_backend.utils import rate_limit
from .models import Category, Equipment
from .serializers import CategorySerializer, EquipmentSerializer
from rest_framework.response import Response
from rest_framework import status


class ReadOnlyOrAdminPermission(IsAuthenticated):
    """
    Custom permission to allow:
    - Authenticated users to read (GET, HEAD, OPTIONS).
    - Admin users to perform all actions.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['eqname', 'description', 'category__categoryname']
    ordering_fields = ['stock', 'eqname']
    ordering = ['eqname']  # Default ordering

    @rate_limit(requests=10, window=60) 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Equipment deleted successfully."}, status=status.HTTP_200_OK)
    
    @rate_limit(requests=20, window=60)  # 20 equipment operations per minute
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @rate_limit(requests=20, window=60)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)