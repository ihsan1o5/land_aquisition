from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import unathenticated_user


@unathenticated_user
def registerView(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Add user to 'customer' group
            customer_group = Group.objects.get(name='customer')
            user.groups.add(customer_group)

            messages.success(request, 'Account has been created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unathenticated_user
def loginView(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username of Password is incorrect!')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')
