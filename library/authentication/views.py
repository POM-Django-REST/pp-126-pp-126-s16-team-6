from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .forms import AddUserForm, UpdateUserForm
from .serializers import UserSerializer


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST.get('middle_name', '')
        email = request.POST['email']
        password = request.POST['password']
        role = int(request.POST['role'])  # 0 = visitor, 1 = librarian

        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse('User with this email already exists.')

        if role == 0:
            user = CustomUser.objects.create_user(
                email=email, password=password,
                first_name=first_name, last_name=last_name,
                middle_name=middle_name, role=role
            )
        elif role == 1:
            user = CustomUser.objects.create_superuser(
                email=email, password=password,
                first_name=first_name, last_name=last_name,
                middle_name=middle_name, role=role,
                is_staff=True, is_superuser=True
            )

        return redirect('login')

    return render(request, 'authentication/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            return HttpResponse('Invalid credentials.')

    return render(request, 'authentication/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


class UserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'object_list'

    # def get_queryset(self):
    #     queryset = CustomUser.objects.all()
    #
    #     title = self.request.GET.get('title', '')
    #     author_name = self.request.GET.get('author_name', '')
    #
    #     if title:
    #         queryset = queryset.filter(name__icontains=title)
    #
    #     if author_name:
    #         queryset = queryset.filter(author__name__icontains=author_name)
    #
    #     return queryset


class UserDetailsView(DetailView):
    model = CustomUser
    template_name = 'user_details.html'
    context_object_name = 'customuser'


class AddUserView(CreateView):
    model = CustomUser
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('user_list')


class UpdateUserView(UpdateView):
    model = CustomUser
    template_name = 'update_user.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('user_list')


class DeleteUserView(DeleteView):
    model = CustomUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('user_list')


class UserAPIListView(APIView):
    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'middle_name': request.data.get('middle_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'role': request.data.get('role'),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIDetailView(APIView):
    def get(self, request, id=None):
        try:
            user = CustomUser.objects.get(pk=id)
            serializer = UserSerializer(user)
        except CustomUser.DoesNotExist:
            return Response({'status': f'User with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        if id is None:
            return Response({'status': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(pk=id)
            user.delete()
        except CustomUser.DoesNotExist:
            return Response({'status': f'User with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id=None):
        if id is None:
            return Response({'status': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'status': f'User with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
