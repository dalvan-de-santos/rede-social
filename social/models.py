from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError




class Profile(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    foto = models.ImageField(blank=True, upload_to='pictures/%Y/%m')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_user.username
    



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(id_user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Post(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    foto = models.ImageField(blank=True, upload_to='pictures_posts/%Y/%m')
    resumo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_user.username



class Likes(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    data_criacao = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('id_user', 'id_post')

    def __str__(self):
        return self.id_user.username


class Followers(models.Model):
    id_seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    id_seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_seguidor', 'id_seguido')
    
    def clean(self):
        if self.id_seguidor == self.id_seguido:
            raise ValidationError("Vc não pode seguir a si mesmo!!!")

    def __str__(self):
        return self.id_seguido.username

