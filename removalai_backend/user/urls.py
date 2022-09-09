from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('history/', views.history, name='history'),
    path('profile/', views.UserProfile, name='profile'),
    path('info-update/', views.InfoUpdate, name='info-update'),
    path('pass-update/', views.PassUpdate, name='pass-update'),
]