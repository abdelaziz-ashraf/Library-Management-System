from django.shortcuts import redirect, render

from lms_app.models import Book, Category
from .forms import BookForm, CategoryForm

# Create your views here.

def index(request):

    if request.method == 'POST':
        new_book = BookForm(request.POST, request.FILES)
        if new_book.is_valid():
            new_book.save()
        new_category = CategoryForm(request.POST)
        if new_category.is_valid():
            new_category.save()

    context = {
        'books' : Book.objects.all(),
        'category' : Category.objects.all(),
        'book_form' : BookForm(),
        'category_form' : CategoryForm(),
        'books_number' : Book.objects.filter(active=True).count(),
        'books_number_rented' : Book.objects.filter(status='rented').count(),
        'books_number_sold' : Book.objects.filter(status='sold').count(),
        'books_number_available' : Book.objects.filter(status='available').count(),
    }

    return render(request, 'pages/index.html', context)

def books(request):

    search = Book.objects.all()
    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains=title)

    context = {
        'books' : search,
        'category' : Category.objects.all(),
        'category_form' : CategoryForm(),
    }

    return render(request, 'pages/books.html', context)

def update(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        book_update = BookForm(request.POST, request.FILES, instance=book)
        if book_update.is_valid():
            book_update.save()
            return redirect('/')
    else:
        book_update = BookForm(instance=book)
    
    context = {
        'form' : book_update,
    }


    return render(request, 'pages/update.html', context)

def delete(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        book.delete()
        return redirect('/')

    return render(request, 'pages/delete.html')
     