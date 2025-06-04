from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save




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
    foto = models.ImageField(blank=True, upload_to='pictures_posts/%Y/m')
    resumo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_user.username


