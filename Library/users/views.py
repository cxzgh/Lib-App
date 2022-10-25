from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.apps import apps
import datetime
from django.db.models import Q

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account is created.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, id):
    order_model = apps.get_model('books', 'Order')
    bookdata_model = apps.get_model('books', 'BookData')
    log_model = apps.get_model('books', 'Log')
    if request.user.is_authenticated:
        request.user.id = id
        order = order_model.objects.filter(user_id=id)
        bookdata = bookdata_model.objects.all()

        if 'give_back' in request.POST.keys():
            book_ids = request.POST.getlist('book_id')
            for book_id in book_ids:
                l = book_id.split("/")
                b = int(l[0])
                o = int(l[1])
                update_return = bookdata_model.objects.get(id=b)
                update_return.book_qt = update_return.book_qt + 1
                update_return.save()
                orders = order_model.objects.filter(Q(id=o) & Q(book=update_return))
                for ord in orders:
                    ord.status = 'returned'
                    ord.save()

                log_update = log_model.objects.get(Q(order_id=o) & Q(status="active"))
                log_entry = log_model.objects.create(order_id=log_update.order_id, user_id=log_update.user_id, book_id=log_update.book_id, borrow_date=log_update.borrow_date, borrow_due=log_update.borrow_due, status='returned')
                log_entry.save()

        if 'renew' in request.POST.keys():
            book_ids = request.POST.getlist('book_id')
            for book_id in book_ids:
                l = book_id.split("/")
                b = int(l[0])
                o = int(l[1])
                update_renew = bookdata_model.objects.get(id=b)
                orders = order_model.objects.filter(Q(id=o) & Q(book=update_renew))
                for ords in orders:
                    ords.borrow_due = ords.borrow_due + datetime.timedelta(days=10)
                    ords.save()

                log_update = order_model.objects.filter(Q(id=o) & Q(status='active'))
                for log in log_update:
                    log_entry = log_model.objects.create(order_id=o, user_id=log.user_id, book_id=log.book.id, borrow_date=str(log.borrow_date)[:-13], borrow_due=str(log.borrow_due)[:-13], status='renew')
                    print()
                    log_entry.save()
        context = {
            'order': order,
            'bookdata': bookdata,
            'date': datetime.datetime.now(),
        }
        return render(request, 'users/profile.html', context)
    else:
        return render(request, 'users/profile.html')
