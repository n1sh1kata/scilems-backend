from django.urls import path
from .views import CartListCreateView, CartUpdateDeleteView, CartDeleteAllView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart_list_create'),
    path('<int:pk>/', CartUpdateDeleteView.as_view(), name='cart_update_delete'),
    path('delete-all/', CartDeleteAllView.as_view(), name='cart_delete_all'),
]