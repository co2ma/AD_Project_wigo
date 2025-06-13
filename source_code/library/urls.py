from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:book_id>/history/', views.BookHistoryView.as_view(), name='book_history'),
    # DRF API
    path('api/books/', views.api_book_list, name='api_book_list'),
    path('api/books/<int:book_id>/', views.api_book_detail, name='api_book_detail'),
    path('api/books/<int:book_id>/history/', views.api_book_history, name='api_book_history'),
] 