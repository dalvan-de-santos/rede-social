from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post, Followers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import ProfileForm
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib import messages



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



@login_required(login_url='homepage')
def profile(resquest):
    profile = resquest.user.profile
    post = Post.objects.filter(id_user = resquest.user).order_by("data_criacao")


    return render(resquest, 'profile.html', {'profile': profile, 'posts': post})

@login_required(login_url='homepage')
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

@login_required(login_url='homepage')
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

@login_required(login_url='homepage')
def pagina_inicial(resquest):
    seguidos_ids = Followers.objects.filter(id_seguidor=resquest.user).values_list('id_seguido', flat=True)

    posts = Post.objects.filter(id_user__in=seguidos_ids).select_related('id_user').order_by('data_criacao')
    print(posts)
    

    return render(resquest, 'pagina_inicial.html', {'posts': posts})


@login_required(login_url='homepage')
def toggle_follow(resquest, username):
    alvo = get_object_or_404(User, username=username)

    if resquest.user == alvo:
        messages.error(resquest, "VC NÃO PODE SEGUIR A SI MESMO")
        return redirect('perfil_detail', username=username)
    
    rel, created = Followers.objects.get_or_create(
        id_seguidor=resquest.user,
        id_seguido=alvo
    )

    if not created:
        rel.delete()
        messages.success(resquest, f"VC DEIXOU DE SEGUIR {alvo.username}")
    
    else:
       messages.success(resquest, f"VC ESTA SEGUINDO {alvo.username}")
    return redirect('perfil_detail', username=username) 


@login_required(login_url='homepage')
def explorar(resquest):
    perfis = Profile.objects.select_related('id_user').only(
        'foto', 'id_user__username'
    )

   
    return render(resquest, 'explorar.html', {'perfis': perfis,} )

@login_required(login_url='homepage')
def perfil_detail(resquest, username):
    perfil = get_object_or_404(Profile, id_user__username=username)
    posts = Post.objects.filter(id_user=perfil.id_user).order_by('data_criacao')

    is_self = perfil.id_user == resquest.user
    is_following = False
    if not is_self:
        is_following = Followers.objects.filter(id_seguidor=resquest.user, id_seguido=perfil.id_user).exists()
    
    
    return render(resquest, 'perfil_detail.html', {'profile': perfil, 'posts': posts, 'is_self': is_self, 'is_following': is_following})


def apagar_post(resquest, id_post):
    post = Post.objects.get(id=id_post)
    post.delete()
    return redirect('profile')