from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None,password2=None):
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError('user must have an username')
        # if password!=confirm_password:
        #    raise ValueError('password and confirm password must be same')
            

        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name, )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(email=self.normalize_email(email),username=username,
                         first_name=first_name,last_name=last_name,password=password)
        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=100,blank=True)
    last_name=models.CharField(max_length=100,blank=True)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=100,blank=True)

    # required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']

    objects=MyAccountManager()

    def full_name(self):
        return f"{self.first_name}{self.last_name}"


    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

# any type of user can watch the module

