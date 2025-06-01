from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



def homepage(resquest):
    return render(resquest, 'homepage.html')


def create_user(resquest):
    if resquest.method == "GET":
        return render(resquest, 'create_user.html')
    
    if resquest.method == "POST":
        username = resquest.POST.get('username')
        email = resquest.POST.get('email')
        senha = resquest.POST.get('senha')

        user = User.objects.filter(username=username)
        if user.exists():
            return HttpResponse("Ja existe um usuario com esse nome")
        user = User.objects.filter(email=email)
        if user.exists():
            return HttpResponse("Ja existe um usuario com esse email")
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        login(resquest, user)
        return redirect('profile')



@login_required
def profile(resquest):
    profile = resquest.user.profile
    return render(resquest, 'profile.html', {'profile': profile})

@login_required
def editar_profile(resquest):
    return HttpResponse('Editar perfil')
