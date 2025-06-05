from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import ProfileForm
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout



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
    post = Post.objects.filter(id_user = resquest.user).order_by("data_criacao")
    return render(resquest, 'profile.html', {'profile': profile, 'posts': post})

@login_required
def editar_profile(resquest):
    profile, _ = Profile.objects.get_or_create(id_user=resquest.user)

    if resquest.method == 'POST':
        form = ProfileForm(resquest.POST, resquest.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:    
        form = ProfileForm(instance=profile)
    return render(resquest, 'editar_profile.html', {'form': form})


def login_user(resquest):
    if resquest.method == 'POST':
        form = AuthenticationForm(resquest, data=resquest.POST)
        if form.is_valid():
            login(resquest, form.get_user())
            return redirect('profile')
    else:   
        form = AuthenticationForm()


    return render(resquest, 'login.html', {'form': form})


def logout_user(resquest):
    logout(resquest)
    return redirect('login_user')

@login_required
def criar_post(resquest):
    if resquest.method == 'POST':
        form = PostForm(resquest.POST, resquest.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.id_user = resquest.user
            post.save()
            return redirect('profile')
    else:
        form = PostForm()

    return render(resquest, 'criar_post.html', {'form': form})