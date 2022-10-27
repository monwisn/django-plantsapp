from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'authentication'
urlpatterns = [
    path('', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_email, name='activate'),
    path('edit-register/', views.edit_register, name='edit_register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('change-password/', views.change_password, name='change_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
    path('set-password/', views.set_password, name='set_password'),
]
