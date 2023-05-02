from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ads import views

urlpatterns = [
    path('', views.CreateView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view()),
    path('create/', views.CategoryCreateView.as_view()),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view()),
]