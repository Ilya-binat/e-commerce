from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        # Генерация уникального username
        base_username = email
        username = base_username
        counter = 1

        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        extra_fields.setdefault("username", username)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  # Если username не указан, задаем его как email
            self.username = self.email
        super().save(*args, **kwargs)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь.",
        verbose_name="группы",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_permission_set",
        blank=True,
        help_text="Конкретные разрешения для пользователя.",
        verbose_name="права пользователя",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class EmailVerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < now() - timedelta(minutes=10)
