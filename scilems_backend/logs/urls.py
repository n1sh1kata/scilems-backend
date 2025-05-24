from django.urls import path
from .views import TransactionLogListView

urlpatterns = [
    path('', TransactionLogListView.as_view(), name='transaction_logs'),
]