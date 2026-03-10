from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('gallery/', views.gallery_view, name='gallery'),
]
