from django.urls import path
from . import views

# from .views import NewsletterUserListView, NewsletterUserDetailView
# from .api_views import CreateNewsletterUserApiView


app_name = 'main'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.about, name='about'),
    path('user/create/', views.create_user_profile, name='create_user_profile'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/sign-up/', views.newsletter_signup, name='newsletter_sign_up'),
    path('newsletter/unsubscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/users/', views.newsletter_users, name='newsletter_users'),
    path('newsletter/users-delete/<str:pk>/', views.newsletter_user_delete, name='newsletter_users_delete'),
    path('change-language/', views.change_language, name='change_language'),
    path('policy/', views.policy, name='policy'),
    path('accept-cookie-policy/', views.accept_cookie_policy, name='accept_cookie_policy'),
    path('cookie-banner/', views.cookie_banner, name='cookie_banner'),
    path('location/', views.api_location, name='api_location'),
    path('translate/', views.translate_app, name='translate_app'),
    path('accounts/social/signup/', views.signup_redirect, name='signup_redirect'),
    # path('newsletter/users/create/', CreateNewsletterUserApiView.as_view(), name='create_newsletter_user'),
    # path('newsletter/users/', NewsletterUserListView.as_view, name='newsletter_users'),
    # path('newsletter/users/<int:id>/', NewsletterUserDetailView.as_view, name='newsletter_user_detail'),
    path('api-avatars/', views.api_avatars, name='api_avatars'),
    path('show-avatars/', views.show_avatars, name='show_avatars'),
]
