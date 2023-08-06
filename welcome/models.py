from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):

  def _create_user(self, email, password, type, is_staff, is_superuser,  **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now,
        type = type, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, type, False, False, **extra_fields)

  def create_superuser(self, email, password, type, **extra_fields):
    user=self._create_user(email, password, type, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=3, choices=[('tut', 'tutor'),('stu', 'student')], default = "")
    classes_signed_up = set()
    rate = models.DecimalField(max_digits=5, decimal_places = 2, default = 5.00)
    bio = models.TextField(null=True, blank=True, default = 'No bio yet')
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['type']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
  
class Schedule(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = ArrayField(models.CharField(max_length=50, blank = True))
    tutorTimings = ArrayField(models.CharField(max_length=50, blank = True))

class Request(models.Model):
   student = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'student')
   tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor')
   course = models.CharField(max_length=254, null=True, blank=True)
   time = models.CharField(max_length=254, null=True, blank=True)
   accepted = models.CharField(max_length=3, choices=[('acc', 'accept'),('dec', 'decline'), ("", "none")], default = "")

class classRequest(models.Model):
    course = models.CharField(max_length=254, null=True, blank=True)
    tutorsAccepted = models.IntegerField(default=0)
    tutorsAlreadyAccepted = ArrayField(models.CharField(max_length=50, blank = True))
    upvotes = models.IntegerField(default=1)
    studentRequested = ArrayField(models.CharField(max_length=50, blank = True))