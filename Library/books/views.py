import requests
from django.shortcuts import render, redirect
from .models import BookData, Order
from django.contrib.auth.decorators import login_required
from .forms import BookDataForm
from django.core.paginator import Paginator

# Create your views here.


def homepage(request):

    book_objects = BookData.objects.all().order_by('book_title')
    book_name = request.GET.get('book_title')
    if book_name != '' and book_name is not None:
        book_objects = book_objects.filter(book_title__icontains=book_name)
    paginator = Paginator(book_objects, 10)
    page = request.GET.get('page')
    book_objects = paginator.get_page(page)
    context = {
        'bookdata': book_objects,
    }
    return render(request, 'books/homepage.html', context)


@login_required
def add_book(request):
    if request.method == "POST":
        if 'confirm' in request.POST.keys():
            book = request.POST['book']
            author = request.POST['author']
            publish_date = request.POST['publish_date']
            isbn = request.POST['isbn']
            qt = request.POST['quantity']
            new_book = BookData(book_title=book, book_author=author, book_publish_date=publish_date, book_ISBN=isbn, book_qt=qt)
            new_book.save()
        else:
            book_input = request.POST['book']
            book_name = book_input.replace(" ", "+")

            response = requests.get(url=f"https://www.googleapis.com/books/v1/volumes?q={book_name}")
            response.raise_for_status()

            title = response.json()["items"][0]["volumeInfo"]["title"]
            author = response.json()["items"][0]["volumeInfo"]["authors"][0]
            publish_date = response.json()["items"][0]["volumeInfo"]["publishedDate"]
            isbn = response.json()["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"]

            context = {
                'title': title,
                'author': author,
                'publish_date': publish_date,
                'isbn': isbn
            }
            return render(request, 'books/add_confirmation.html', context)
    return render(request, 'books/add.html')


def add_confirm(request):
    if request.method == "POST":
        return render(request, 'books/add_confirmation.html')


def librarian(request):
    book_objects = BookData.objects.all().order_by('book_title')

    book_name = request.GET.get('book_title')

    if book_name != '' and book_name is not None:
        book_objects = book_objects.filter(book_title__icontains=book_name)

    paginator = Paginator(book_objects, 10)
    page = request.GET.get('page')
    book_objects = paginator.get_page(page)

    context = {
            'bookdata': book_objects,
    }
    return render(request, 'books/librarian.html', context)


def delete_book(request, id):
    book = BookData.objects.get(pk=id)
    if request.method == 'POST':
        book.delete()
        context = {
            'bookdata': BookData.objects.all()
        }
        return redirect('homepage')

    return render(request, 'books/delete_book.html', {'book': book})


def edit_book(request, id):
    book = BookData.objects.get(pk=id)
    form = BookDataForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('librarian_page')
    else:
        return render(request, 'books/edit.html', {'form': form, 'book': book})


def borrow_book(request, id):
    book = BookData.objects.get(pk=id)
    book_quantity = book.book_qt
    if book_quantity >= 1:
        if request.method == "POST":
            if request.user.is_authenticated:
                current_user_id = request.user.id

                new_order = Order.objects.create(user_id=current_user_id, book=book)
                new_order.save()

                book.book_qt = book_quantity - 1
                book.save()
                return redirect('homepage')
    else:
        return redirect('out_of_order')

    context = {
        'book_all': BookData.objects.all(),
        'book': book
    }
    return render(request, 'books/borrow.html', context)


def out_of_order(request):
    return render(request, 'books/out_of_order.html')


def details(request, id):
    book = BookData.objects.get(pk=id)
    context = {
        'book': book
    }
    return render(request, 'books/details.html', context)