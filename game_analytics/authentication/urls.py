# auth/urls.py
from django.urls import path
from .views import register, login_view, logout_view
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login_view'),
    path('auth/logout/', logout_view, name='logout_view'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
 