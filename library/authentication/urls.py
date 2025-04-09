from django.urls import path
from .views import (register, user_login, user_logout, UserListView, UserDetailsView,
                    AddUserView, UpdateUserView, DeleteUserView, UserAPIListView, UserAPIDetailView)


urlpatterns = [
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('user_list/', UserListView.as_view(), name="user_list"),
    path('user_details/<int:pk>', UserDetailsView.as_view(), name="user_details"),
    path('add_user/', AddUserView.as_view(), name="add_user"),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name="update_user"),
    path('delete_user/<int:pk>', DeleteUserView.as_view(), name="delete_user"),
    path('user/', UserAPIListView.as_view()),
    path('user/<int:id>', UserAPIDetailView.as_view()),
]