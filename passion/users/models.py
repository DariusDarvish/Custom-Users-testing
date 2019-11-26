from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    # fields requried to create a user
    # place everything before password
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users need a username")

        user_obj = self.model(
            # normalize makes everything lowercase in the database
            email=self.normalize_email(email),

        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    # superuser object
    def create_superuser(self, email, password=None):
        user = self.create_user(
            # normalize makes everything lowercase in the database

            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
            is_superuser=True

        )

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # unique allows for only one email of that name like a set
    # fields I want to Implement
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=150)
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    # required fields
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # this is what we will set as the login parameter including password
    USERNAME_FIELD = 'email'
    # Required fields for registering
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_active

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active

    # required functions for Custom User
    # 1.if a user is an admin
    def has_perm(self, perm, obj=None):
        return True

    # 2. they can change data in the database
    def has_module_perms(self, app_label):
        return True
