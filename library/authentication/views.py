from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import AddUserForm, UpdateUserForm


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
