from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def get(self, *args, **kwargs):
        return super().select_related('profile').get(*args, **kwargs)

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a User with an email and a password."""

        if not email:
            raise ValueError('Users must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with an email and a password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


