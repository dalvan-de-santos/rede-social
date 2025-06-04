from django.urls import path
from .import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create_user/', views.create_user, name='create_user'),
    path('profile/', views.profile, name='profile'),
    path('editar_profile', views.editar_profile, name='editar_profile'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('criar_post', views.criar_post, name='criar_post')
]
