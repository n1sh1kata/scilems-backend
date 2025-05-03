from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProtectedView, AdminOnlyView, LogoutView
from scilems_backend.utils import rate_limit

class RateLimitedTokenObtainPairView(TokenObtainPairView):
    @rate_limit(requests=3, window=60)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', RateLimitedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('logout/', LogoutView.as_view(), name='logout'),
]