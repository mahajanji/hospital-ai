from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_views, name='login_views'),
    path('register/', views.register_views, name='register_views'),
]
