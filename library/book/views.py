from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .forms import AddBookForm, UpdateBookForm
from .serializers import BookSerializer


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'object_list'
    fields = ['name']

    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.GET.get('title', '')
        author_name = self.request.GET.get('author_name', '')

        if title:
            queryset = queryset.filter(name__icontains=title)

        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)

        return queryset


class BookDetailsView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'


class AddBookView(CreateView):
    model = Book
    template_name = 'add_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('book_list')


class UpdateBookView(UpdateView):
    model = Book
    template_name = 'update_book.html'
    form_class = UpdateBookForm
    success_url = reverse_lazy('book_list')


class DeleteBookView(DeleteView):
    model = Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('book_list')


class UserBookListView(ListView):
    model = Book
    template_name = "book/user_books_list.html"
    context_object_name = "books"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Book.objects.filter(user__id=user_id)


class BookAPIListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'author': request.data.get('author'),
            'description': request.data.get('description'),
            'count': request.data.get('count'),
            'publication_year': request.data.get('publication_year'),
            'issue_date': request.data.get('issue_date'),
        }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAPIDetailView(APIView):
    def get(self, request, id=None):
        try:
            book = Book.objects.get(pk=id)
            serializer = BookSerializer(book)
        except Book.DoesNotExist:
            return Response({'status': f'Book with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        if id is None:
            return Response({'status': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(pk=id)
            book.delete()
        except Book.DoesNotExist:
            return Response({'status': f'Book with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id=None):
        if id is None:
            return Response({'status': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response({'status': f'Book with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
