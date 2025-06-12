from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cv/', views.view_cv, name='view_cv'),
    path('blog', views.blog_list, name='blog_list'),
    path('blog/add', views.blog_add, name='blog_add'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
] 