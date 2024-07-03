from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from api.models.hotel_models import Hotel
from api.utils.base_model import BaseModel

class CustomManager(BaseUserManager):
    """_Custom user model  to use email as username 
    """
    
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        
        if extra_fields.setdefault("is_staff") is not True or extra_fields.setdefault("is_superuser") is not True:
            raise ValueError("Superusers must have is_staff and is_superuser properties set set to True")
        
        return self.create_user(email,password,**extra_fields)
        
   
class User(AbstractUser,BaseModel):
    username=None
    email=models.EmailField(_("email_address"),unique=True)
    first_name=models.CharField(max_length=255,blank=True),
    last_name=models.CharField(max_length=255,blank=True),
    USERNAME_FIELD="email"
    REQUIRED_FIELDS =[]
    objects=CustomManager()
    
    
    def __str__(self) -> str:
        return self.email