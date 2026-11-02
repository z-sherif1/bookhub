
from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
)

urlpatterns = [
    # Register
    path('signup/', views.signup, name='signup'),

    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # Login
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login',
    ),

    # Password change
    path(
        'change-password/',
        views.BookHubPasswordChangeView.as_view(),
        name='change_password',
    ),

    # Password change done
    path(
        'change-password/done/',
        PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done',
    ),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UpdateProfileView.as_view(), name='edit_profile'),
]
