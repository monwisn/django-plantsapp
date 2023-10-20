from django.urls import path

from galleries import views


app_name = "galleries"
urlpatterns = [
    path('', views.galleries_list, name="list"),
    path('add-gallery/', views.add_gallery, name='add_gallery'),
    path('<int:gallery_id>', views.gallery_details, name="details"),
    path('<int:gallery_id>/add/', views.add_photos, name='add_photos'),
    path('gallery-edit/<int:pk>', views.gallery_edit, name='gallery_edit'),
    path('gallery-delete/<int:pk>', views.gallery_delete, name='gallery_delete'),
    path('galleries-list-admin/', views.galleries_list_admin, name='galleries_list_admin'),
    path('galleries-list-view/', views.galleries_list_view, name='galleries_list_view'),
    path('galleries-list-view/<int:gallery_id>', views.photos_view, name='photos_view'),
    path('photo-delete/<int:pk>', views.photo_delete, name='photo_delete'),
    path('<int:pk>/photos-edit/', views.PhotosEditView.as_view(), name='photos_edit'),
    path('test-galleries/', views.test_galleries, name='test_galleries'),
]