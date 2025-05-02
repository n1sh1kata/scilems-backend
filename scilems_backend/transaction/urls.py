from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction_detail'),
]