from django.contrib.auth.views import LogoutView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path

from apps.accounts import views as v

urlpatterns = [
    path('user/edit/', v.ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<slug:slug>/', v.ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', v.UserRegisterView.as_view(), name='register'),
    path('login/', v.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', v.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', v.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', v.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
