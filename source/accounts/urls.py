from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import RegistrationView, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
]
