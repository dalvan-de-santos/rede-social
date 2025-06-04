from django.contrib import admin
from .models import Profile, Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'bio', 'foto', 'data_criacao')
    ordering = ('id_user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'foto', 'resumo', 'data_criacao')
    ordering = ('id_user',)

