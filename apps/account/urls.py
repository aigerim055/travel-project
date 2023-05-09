from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegistrationView,
    PhoneActivationView,
    EmailActivationView,
    ChangePasswordView,
    SetRestoredPasswordView,
    RestorePasswordView,
    DeleteAccountView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registartion'),
    path('activate/<str:activation_code>/', EmailActivationView.as_view(), name='activation'),
    path('activate/', PhoneActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('restore-password/', RestorePasswordView.as_view(), name='restore_pasword'),
    path('set-restored-password/', SetRestoredPasswordView.as_view(), name='set_restored_password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete account'),
]