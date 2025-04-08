# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Author
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm

class AuthorListView(ListView):
    model = Author
    template_name = "author_list.html"
    context_object_name = "authors"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
    
@login_required
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')  
    else:
        form = AuthorForm()

    return render(request, 'create_author.html', {'form': form})

@login_required
def remove_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    # Only allow deletion if the author is not attached to any books
    if author.books.count() == 0:
        author.delete()
        return redirect('author_list')  # Redirect to the author list page after removal
    return render(request, 'remove_author_failed.html', {'author': author})