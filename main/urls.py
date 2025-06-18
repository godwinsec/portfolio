from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cv/', views.view_cv, name='view_cv'),
    path('blog', views.blog_list, name='blog_list'),
    path('blog/add', views.blog_add, name='blog_add'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    # Froala image upload endpoints
    path('upload_image/', views.upload_image, name='upload_image'),
    path('load_images/', views.load_images, name='load_images'),
    path('delete_image/', views.delete_image, name='delete_image'),
] 