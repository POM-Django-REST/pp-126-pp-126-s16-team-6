from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='author_list'),
    path('create-author/', views.create_author, name='create_author'),  
    path('remove-author/<int:author_id>/', views.remove_author, name='remove_author'),  
]
