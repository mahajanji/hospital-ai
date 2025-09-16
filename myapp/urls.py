from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.submit_contact, name='submit_contact'),
    path('login/', views.login_views, name='login_views'),
    path('register/', views.register_views, name='register_views'),
    path('api/chatbot/', views.chatbot_reply, name='chatbot_reply'),
    
]
