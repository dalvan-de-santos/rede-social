from django.urls import path
from .import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create_user/', views.create_user, name='create_user'),
    path('usuario/<int:id_user>/follow', views.toggle_follow, name='toggle_follow'),
    path('profile/', views.profile, name='profile'),
    path('editar_profile', views.editar_profile, name='editar_profile'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('criar_post', views.criar_post, name='criar_post'),
    path('pagina_inicial', views.pagina_inicial, name='pagina_inicial'),
    path('explorar/', views.explorar, name='explorar'),
    path('perfil/<str:username>/', views.perfil_detail, name='perfil_detail'),
    
    
]
