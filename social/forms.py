from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'foto']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte um pouco sobre vc'}),
        }