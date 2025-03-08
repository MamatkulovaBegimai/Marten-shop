from django.urls import path
from django.contrib.auth import views as auth_views

from user.views import RegisterView, MyAccountView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', MyAccountView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
