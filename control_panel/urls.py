from django.urls import path

from . import views


app_name = 'control_panel'
urlpatterns = [
    path('newsletter/', views.control_newsletter, name='control_newsletter'),
    path('newsletter-list/', views.control_newsletter_list, name='control_newsletter_list'),
    path('newsletter-detail/<int:pk>', views.control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-edit/<int:pk>', views.control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-delete/<int:pk>', views.control_newsletter_delete, name='control_newsletter_delete'),
    path('carousel/', views.control_carousel, name='control_carousel'),
    path('carousel-list/', views.control_carousel_list, name='control_carousel_list'),
    path('carousel-delete/<int:pk>', views.control_carousel_delete, name='control_carousel_delete'),
]
