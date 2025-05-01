from django.urls import path
from .views import index_view, logout_view, register_view, login_view, protected_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('', index_view, name='index'),
    path('protected/', protected_view, name='protected'),
    path('logout/', logout_view, name='logout'),
]