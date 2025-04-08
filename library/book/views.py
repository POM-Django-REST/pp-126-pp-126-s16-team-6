from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from .forms import AddBookForm, UpdateBookForm


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
