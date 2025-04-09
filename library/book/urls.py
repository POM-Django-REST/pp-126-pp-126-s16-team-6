from django.urls import path
from .views import BookListView, BookDetailsView, AddBookView, UpdateBookView, DeleteBookView, UserBookListView, \
    BookAPIListView, BookAPIDetailView

urlpatterns = [
    path('', BookListView.as_view(), name="book_list"),
    path('book_details/<int:pk>', BookDetailsView.as_view(), name="book_details"),
    path('add_book/', AddBookView.as_view(), name="add_book"),
    path('update_book/<int:pk>', UpdateBookView.as_view(), name="update_book"),
    path('delete_book/<int:pk>', DeleteBookView.as_view(), name="delete_book"),
    path('user/<int:user_id>/books/', UserBookListView.as_view(), name='user_books_list'),
    path('book/', BookAPIListView.as_view()),
    path('book/<int:id>', BookAPIDetailView.as_view()),
]
