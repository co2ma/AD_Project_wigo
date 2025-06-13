from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView, DetailView
from library.services import book_service
from library.exceptions import BookNotFound, BookHasNoBorrowHistory
from library.models import Book, BorrowHistory
from django.contrib.auth.models import User

# Create your views here.

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

class BookHistoryView(DetailView):
    model = Book
    template_name = 'library/book_history.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            book = self.get_object()
            histories = book_service.get_borrow_history_for_book(book)
            context['histories'] = histories
        except BookHasNoBorrowHistory as e:
            context['message'] = str(e)
            context['histories'] = []
        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except BookNotFound as e:
            return HttpResponseNotFound(str(e))

# DRF API: 책 목록
@api_view(['GET'])
def api_book_list(request):
    books = Book.objects.all().values('id', 'title', 'author', 'isbn', 'created_at')
    return Response(list(books))

# DRF API: 단일 책
@api_view(['GET'])
def api_book_detail(request, book_id):
    try:
        book = Book.objects.values('id', 'title', 'author', 'isbn', 'created_at').get(id=book_id)
        return Response(book)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

# DRF API: 책의 대출 이력
@api_view(['GET'])
def api_book_history(request, book_id):
    try:
        book = book_service.get_book_by_id(book_id)
        histories = book_service.get_borrow_history_for_book(book)
        data = [
            {
                'user': h.user.username,
                'borrowed_at': h.borrowed_at,
                'returned_at': h.returned_at
            } for h in histories
        ]
        return Response(data)
    except BookNotFound as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except BookHasNoBorrowHistory as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
