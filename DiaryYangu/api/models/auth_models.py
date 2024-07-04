from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from api.utils.base_model import BaseModel

class CustomManager(BaseUserManager):
    """_Custom user model  to use email as username 
    """
    
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Ensure you are using the correct database manager
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
    # first_name=models.CharField(max_length=255,blank=True,null=True),
    # last_name=models.CharField(max_length=255,blank=True,null=True),
    age=models.IntegerField(blank=True,null=True),
    USERNAME_FIELD="email"
    REQUIRED_FIELDS =[]
    objects=CustomManager()
    
    
    def __str__(self) -> str:
        return(f"{self.first_name} {self.last_name}")
    
    
class UserProfile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self) -> str:
        return(f"{self.user.username}" )
    