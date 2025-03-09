from django.urls import path
from . import views

app_name = 'survey'  # URL Reverse에서 namespace역할을 하게 됩니다.

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('survey/', views.survey, name='survey'),
]
