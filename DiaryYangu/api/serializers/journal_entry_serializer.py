from rest_framework import serializers
from api.models.auth_models import User
from api.models.journal_models import Category,JournalEntry

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["title", "description","description","color"]
        
        
class JournalEntrySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'created_at','categories']

    

