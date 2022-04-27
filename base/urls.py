from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('', views.home, name="home"),
    path('client/<str:pk>/', views.client, name="client"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-client/', views.createClient, name="create-client"),
    path('update-client/<str:pk>/', views.updateClient, name="update-client"),
    path('delete-client/<str:pk>/', views.deleteClient, name="delete-client"),


    path('order/<str:pk>/', views.order, name="order"),

    path('create-order/', views.createOrder, name="create-order"),
    path('update-order/<str:pk>/', views.updateOrder, name="update-order"),
    path('delete-order/<str:pk>/', views.deleteOrder, name="delete-order"),

]