from django import forms
from .models import Profile, Post


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'foto']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte um pouco sobre vc'}),
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['foto', 'resumo']