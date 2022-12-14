import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import BookData, Order, Log
from django.contrib.auth.decorators import login_required
from .forms import BookDataForm
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


def homepage(request):
    book_objects = BookData.objects.all().order_by('book_title')
    book_details = request.GET.get('book_details')
    if book_details != '' and book_details is not None:
        book_objects = book_objects.filter(
            Q(book_title__icontains=book_details) | Q(book_author__icontains=book_details))
    paginator = Paginator(book_objects, 15)
    page = request.GET.get('page')
    book_objects = paginator.get_page(page)

    if request.method == "POST":
        book_input = request.POST['search_book_title']
        book_name = book_input.replace(" ", "+")
        response = requests.get(url=f"https://www.googleapis.com/books/v1/volumes?q={book_name}")
        if 'confirm' in request.POST.keys():
            book = request.POST['book']
            author = request.POST['author']
            publish_date = request.POST['publish_date']
            isbn = request.POST['isbn']
            qt = request.POST['quantity']
            length = request.POST['length']
            description = request.POST['description']
            new_book = BookData(book_title=book, book_author=author, book_publish_date=publish_date, book_ISBN=isbn, book_qt=qt, book_length=length, book_description=description)
            new_book.save()
        elif 'next' in request.POST.keys():
            itemz = request.POST['item']
            item = int(itemz)
            try:
                item += 1
                title = response.json()["items"][item]["volumeInfo"]["title"]
                author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                description = response.json()["items"][item]["volumeInfo"]["description"]
                description_exists = True
            except KeyError:
                description_exists = False
            while not description_exists:
                try:
                    item += 1
                    title = response.json()["items"][item]["volumeInfo"]["title"]
                    author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                    publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                    isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                    length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                    description = response.json()["items"][item]["volumeInfo"]["description"]
                    description_exists = True
                except KeyError:
                    description_exists = False
                if description_exists:
                    context = {
                        'title': title,
                        'author': author,
                        'publish_date': publish_date,
                        'isbn': isbn,
                        'length': length,
                        'description': description,
                        'item': item,
                        'book_input': book_input,
                    }
                    return render(request, 'books/add_confirmation.html', context)
            if description_exists:
                context = {
                    'title': title,
                    'author': author,
                    'publish_date': publish_date,
                    'isbn': isbn,
                    'length': length,
                    'description': description,
                    'item': item,
                    'book_input': book_input,
                }
                return render(request, 'books/add_confirmation.html', context)

        else:
            item = 0
            try:
                description_exists = True
                title = response.json()["items"][item]["volumeInfo"]["title"]
                author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                description = response.json()["items"][item]["volumeInfo"]["description"]
            except KeyError:
                description_exists = False
            if description_exists:
                context = {
                    'title': title,
                    'author': author,
                    'publish_date': publish_date,
                    'isbn': isbn,
                    'length': length,
                    'description': description,
                    'item': item,
                    'book_input': book_input,
                }
                return render(request, 'books/add_confirmation.html', context)
            else:

                while not description_exists:
                    try:
                        item += 1
                        title = response.json()["items"][item]["volumeInfo"]["title"]
                        author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                        publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                        isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                        length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                        description = response.json()["items"][item]["volumeInfo"]["description"]
                        description_exists = True
                    except KeyError:
                        description_exists = False
                    if description_exists is True:
                        context = {
                            'title': title,
                            'author': author,
                            'publish_date': publish_date,
                            'isbn': isbn,
                            'length': length,
                            'description': description,
                            'item': item,
                            'book_input': book_input,
                        }
                        return render(request, 'books/add_confirmation.html', context)

    context = {
        'bookdata': book_objects,
    }
    return render(request, 'books/homepage.html', context)


@login_required
def add_confirm(request):
    return render(request, 'books/add_confirmation.html')


@login_required
def librarian(request):
    book_objects = BookData.objects.all().order_by('book_title')
    book_details = request.GET.get('book_details')
    if book_details != '' and book_details is not None:
        book_objects = book_objects.filter(Q(book_title__icontains=book_details) | Q(book_author__icontains=book_details))

    paginator = Paginator(book_objects, 15)
    page = request.GET.get('page')
    book_objects = paginator.get_page(page)

    if request.method == "POST":
        book_input = request.POST['search_book_title']
        book_name = book_input.replace(" ", "+")
        response = requests.get(url=f"https://www.googleapis.com/books/v1/volumes?q={book_name}")
        if 'confirm' in request.POST.keys():
            book = request.POST['book']
            author = request.POST['author']
            publish_date = request.POST['publish_date']
            isbn = request.POST['isbn']
            qt = request.POST['quantity']
            length = request.POST['length']
            description = request.POST['description']
            new_book = BookData(book_title=book, book_author=author, book_publish_date=publish_date, book_ISBN=isbn, book_qt=qt, book_length=length, book_description=description)
            new_book.save()
        elif 'next' in request.POST.keys():
            itemz = request.POST['item']
            item = int(itemz)
            try:
                item += 1
                title = response.json()["items"][item]["volumeInfo"]["title"]
                author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                description = response.json()["items"][item]["volumeInfo"]["description"]
                description_exists = True
            except KeyError:
                description_exists = False
            while not description_exists:
                try:
                    item += 1
                    title = response.json()["items"][item]["volumeInfo"]["title"]
                    author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                    publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                    isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                    length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                    description = response.json()["items"][item]["volumeInfo"]["description"]
                    description_exists = True
                except KeyError:
                    description_exists = False
                if description_exists:
                    context = {
                        'title': title,
                        'author': author,
                        'publish_date': publish_date,
                        'isbn': isbn,
                        'length': length,
                        'description': description,
                        'item': item,
                        'book_input': book_input,
                    }
                    return render(request, 'books/add_confirmation.html', context)
            if description_exists:
                context = {
                    'title': title,
                    'author': author,
                    'publish_date': publish_date,
                    'isbn': isbn,
                    'length': length,
                    'description': description,
                    'item': item,
                    'book_input': book_input,
                }
                return render(request, 'books/add_confirmation.html', context)

        else:
            item = 0
            try:
                description_exists = True
                title = response.json()["items"][item]["volumeInfo"]["title"]
                author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                description = response.json()["items"][item]["volumeInfo"]["description"]
            except KeyError:
                description_exists = False
            if description_exists:
                context = {
                    'title': title,
                    'author': author,
                    'publish_date': publish_date,
                    'isbn': isbn,
                    'length': length,
                    'description': description,
                    'item': item,
                    'book_input': book_input,
                }
                return render(request, 'books/add_confirmation.html', context)
            else:

                while not description_exists:
                    try:
                        item += 1
                        title = response.json()["items"][item]["volumeInfo"]["title"]
                        author = response.json()["items"][item]["volumeInfo"]["authors"][0]
                        publish_date = response.json()["items"][item]["volumeInfo"]["publishedDate"]
                        isbn = response.json()["items"][item]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                        length = response.json()["items"][item]["volumeInfo"]["pageCount"]
                        description = response.json()["items"][item]["volumeInfo"]["description"]
                        description_exists = True
                    except KeyError:
                        description_exists = False
                    if description_exists is True:
                        context = {
                            'title': title,
                            'author': author,
                            'publish_date': publish_date,
                            'isbn': isbn,
                            'length': length,
                            'description': description,
                            'item': item,
                            'book_input': book_input,
                        }
                        return render(request, 'books/add_confirmation.html', context)

    context = {
            'bookdata': book_objects,
    }
    return render(request, 'books/librarian.html', context)


@login_required
def delete_book(request, id):
    book = BookData.objects.get(pk=id)
    if request.method == 'POST':
        book.delete()
        return redirect('librarian_page')

    return render(request, 'books/delete_book.html', {'book': book})


@login_required
def edit_book(request, id):
    book = BookData.objects.get(pk=id)
    form = BookDataForm(request.POST or None, instance=book)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('librarian_page')

    return render(request, 'books/edit.html', {'form': form, 'book': book})


@login_required
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

                order = Order.objects.latest('id', 'borrow_date', 'status', 'borrow_due')
                log_entry = Log.objects.create(order_id=order.id, user_id=current_user_id, book_id=book.id, borrow_date=str(order.borrow_date)[:-13], borrow_due=str(order.borrow_due)[:-13], status=order.status)
                log_entry.save()

                book_for_message = book.book_title
                messages.success(request, f'You successfully borrowed {book_for_message}.')
                return redirect('homepage')
    else:
        return redirect('out_of_order')

    context = {
        'book_all': BookData.objects.all(),
        'book': book
    }
    return render(request, 'books/borrow.html', context)


@login_required
def out_of_order(request):
    return render(request, 'books/out_of_order.html')


@login_required
def details(request, id):

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

                order = Order.objects.latest('id', 'borrow_date', 'status', 'borrow_due')
                log_entry = Log.objects.create(order_id=order.id, user_id=current_user_id, book_id=book.id, borrow_date=str(order.borrow_date)[:-13], borrow_due=str(order.borrow_due)[:-13], status=order.status)
                log_entry.save()

                book_for_message = book.book_title
                messages.success(request, f'You successfully borrowed {book_for_message}.')
                return redirect('homepage')
    else:
        return redirect('out_of_order')

    context = {
        'book': book
    }
    return render(request, 'books/details.html', context)

@login_required
def logs(request):
    log = Log.objects.all().order_by('-id')
    paginator = Paginator(log, 15)
    page = request.GET.get('page')
    log_pag = paginator.get_page(page)
    context = {
        'logs': log,
        'log_data': log_pag,
        'book': BookData.objects.all(),
    }
    return render(request, 'books/logs.html', context)


def info(request):
    return render(request, 'books/info.html')