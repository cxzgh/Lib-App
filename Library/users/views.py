from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.apps import apps
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


def profile(request, id):
    order_model = apps.get_model('books', 'Order')
    bookdata_model = apps.get_model('books', 'BookData')
    if request.user.is_authenticated:
        request.user.id = id

        order = order_model.objects.filter(user_id=id)
        bookdata = bookdata_model.objects.all()

        context = {
            'order': order,
            'bookdata': bookdata,
        }
        return render(request, 'users/profile.html', context)
    else:
        return render(request, 'users/profile.html')
