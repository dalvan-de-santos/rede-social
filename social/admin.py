from django.contrib import admin
from .models import Profile, Post, Followers


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'bio', 'foto', 'data_criacao')
    ordering = ('id_user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'foto', 'resumo', 'data_criacao')
    ordering = ('id_user',)


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('id','id_seguidor', 'id_seguido', 'data_criacao')
    ordering = ('id',)

