from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from ace.constants import MAX_LENGTH_STANDARDFIELDS, LANGUAGE_CHOICES, LANGUAGE_FLUENCY_CHOICES, YES_NO, CATEGORY_CHOICES
from companies.models import Company
from django.contrib.auth.models import UserManager

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six as six

# Create your models here.
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_email_confirmed) 
        )
account_activation_token = TokenGenerator()

class ApplicationsTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.protect_file_temp_download_key)
        )
downloadProtectedFile_token = ApplicationsTokenGenerator()

class MyUserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, user_type, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not firstName or not lastName:
            raise ValueError("User must have a first and last name")
        if not user_type:
            raise ValueError("User must have an user type")
        user = self.model(
                email=email,
                firstName=firstName,
                lastName=lastName,
                user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, user_type, password):
        user = self.create_user(
                email = email,
                firstName = firstName,
                lastName = lastName,
                password = password,
                user_type = user_type,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser , PermissionsMixin):
    USER_TYPE_CHOICES = (
      (1, 'candidate'),
      (2, 'employer'),
      (3, 'admin'),
      (4, 'super'),
  )
    username = None
    email = models.EmailField(verbose_name='email', max_length = 60, unique=True)
    date_joined = models.DateTimeField(verbose_name='Joined date', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    firstName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    lastName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    protect_file_temp_download_key = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'user_type']

    objects = MyUserManager()

    object = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return (self.is_admin or self.is_superuser)

    def has_module_perms(self, app_label):
        return True

class Candidate(models.Model):

    studentID = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    creditCompleted = models.FloatField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= 0)
    creditLeft = models.FloatField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= 0)
    gpa = models.FloatField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= "")
    program = models.CharField(choices=CATEGORY_CHOICES, max_length = 20, default="ANY")
    internationalStudent = models.CharField(choices=YES_NO, max_length = 3, default="No")
    travel = models.CharField(choices=YES_NO, max_length = 3, default="No")
    timeCommitment = models.CharField(choices=YES_NO, max_length = 3, default="No")
    transcript = models.FileField(upload_to='candidate/transcript/', default="")

    def __str__(self):
        return self.user.email

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= "")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default= "")

    def __str__(self):
        return self.user.email

class PreferredName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= "")
    preferredName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")

    def __str__(self):
        return self.user.email

class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    fluency = models.CharField(choices=LANGUAGE_FLUENCY_CHOICES, max_length = MAX_LENGTH_STANDARDFIELDS,default= "")
    details = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")

    def __str__(self):
        return self.user.email