from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='friend_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def add_friend(self, friend):
        if friend != self:
            self.friends.add(friend)

    def remove_friend(self, friend):
        self.friends.remove(friend)

    def is_friend(self, user):
        return user in self.friends.all()

# Movie model using the custom user
class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=255)
    watched_on = models.DateField()
    REVIEW_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
    review = models.IntegerField(choices=REVIEW_CHOICES, default=3)

    def __str__(self):
        return self.title
