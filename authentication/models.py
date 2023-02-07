from django.db import models
from django.conf import settings

from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,PermissionsMixin)

  
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,**kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
           **kwargs
        )        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username,password,**kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **kwargs
        
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=200,null=False,db_index=True)
    email = models.EmailField(verbose_name="Adresse Email",null=False,primary_key=True, unique=True,db_index=True,db_column='email')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    is_admin = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)   
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
 
    objects=UserManager()  # Telling to Django how to manage objects

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
            return self.is_admin



