from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import markdown

from .managers import CustomUserManager

from imageutils.models import Photo


class CustomUser(AbstractUser):
    username = None
    full_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    def change_name(self, value):
        self.full_name = value


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    display_name = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    using_markdown = models.BooleanField(blank=True, default=False)
    email_confirmed = models.BooleanField(default=False)

    skills = models.ManyToManyField(
        'Skill',
        related_name='profiles'
    )

    @property
    def name(self):
        return self.display_name

    @name.setter
    def name(self, value):
        self.display_name = value

    def get_about(self):
        if self.using_markdown:
            return markdown.markdown(self.about)
        else:
            return self.about

    def __str__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, display_name=instance.full_name)
    instance.profile.save()


class Skill(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
