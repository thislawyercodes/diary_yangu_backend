from api.utils.filters import JournalEntryFilter
from rest_framework import generics, permissions, status
from api.models.journal_models import JournalEntry,Category
from api.serializers.journal_entry_serializer import JournalEntrySerializer,CategorySerializer,CategorizeJournalSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters





class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class JournalEntryListCreateAPIView(generics.ListCreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'id']
    filterset_class = JournalEntryFilter

    ordering_fields = ['created_at']
    
    

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JournalEntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except JournalEntry.DoesNotExist:
            return Response("Journal Entry does not exist", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        journal_entry = self.get_object()
        serializer = self.get_serializer(journal_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        journal_entry = self.get_object()
        journal_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CategorizeJournalView(APIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CategorizeJournalSerializer(data=request.data)
        if serializer.is_valid():
            journal_entry_id = serializer.validated_data['journal_entry_id']
            category_ids = serializer.validated_data['categories']

            try:
                journal_entry = JournalEntry.objects.get(id=journal_entry_id)
            except JournalEntry.DoesNotExist:
                return Response({"error": "Journal entry not found."}, status=status.HTTP_404_NOT_FOUND)

            categories = Category.objects.filter(id__in=category_ids)
            category_title=[category.title for category in categories]

            
            existing_categories = journal_entry.categories.filter(id__in=category_ids)
            if existing_categories.exists():
                return Response({"error": f"Category {category_title} has already been added to this journal entry {journal_entry.title}."}, status=status.HTTP_400_BAD_REQUEST)
            if not categories.exists():
                return Response({"error": "No valid categories found."}, status=status.HTTP_400_BAD_REQUEST)
            

            journal_entry.categories.set(categories)
            journal_entry.save()
            
            return Response({"message": f"Journal entry added to category {category_title}."}, status=status.HTTP_200_OK)
 