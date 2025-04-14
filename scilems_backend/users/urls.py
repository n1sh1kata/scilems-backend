from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from .views import ProtectedView

urlpatterns += [
    path('protected/', ProtectedView.as_view(), name='protected'),
]


# users/urls.py
from .views import LogoutView

urlpatterns += [
    path('logout/', LogoutView.as_view(), name='logout'),
]
