from django.urls import path
from api.views.journal_entry_views import CategoryListCreateAPIView,JournalEntryDetailAPIView,JournalEntryListCreateAPIView

app_name='Journal'

urlpatterns = [
    path('category',CategoryListCreateAPIView.as_view(),name='category'),
     path('new-entry/',JournalEntryListCreateAPIView.as_view(), name='journal-entry-list-create'),
    path('entry/<int:pk>/',JournalEntryDetailAPIView.as_view(), name='journal-entry-detail'),
]
