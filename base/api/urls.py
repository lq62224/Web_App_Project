from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('clients/', views.getClients),
    path('clients/<str:pk>/', views.getClient),

]