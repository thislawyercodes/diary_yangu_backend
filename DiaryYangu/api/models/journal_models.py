from api.models.auth_models import User
from api.utils.base_model import BaseModel
from django.db import models

class Category(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#FFFFFF')  

    def __str__(self):
        return self.title
    
    
class JournalEntry(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=255)
    content = models.TextField(null=True,blank=True)
    categories = models.ManyToManyField(Category, related_name='journal_entries', blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title