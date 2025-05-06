from django.urls import path
from .views import UserProfileListCreateView, UserProfileRetrieveUpdateDestroyView

urlpatterns = [
    path('', UserProfileListCreateView.as_view(), name='userprofile_list_create'),
    path('<int:pk>/', UserProfileRetrieveUpdateDestroyView.as_view(), name='userprofile_detail'),
]