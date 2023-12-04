from django.urls import path
from .views import(
    RegistrationView,
    AccountActivationView
)


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register-account'),
    path('activate/', AccountActivationView.as_view(), name='activate account'),
]
