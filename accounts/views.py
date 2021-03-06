from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid logged in credential')
            return redirect('login')

    return render(request, 'accounts/login.html')


def registration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "User name doesn't exist")
                return redirect('registration')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email doesn't exist")
                    return redirect('registration')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username,
                                                    email=email,
                                                    password=password)
                    auth.login(request, user)
                    user.save()
                    messages.success(request, "You are now login.")
                    return redirect('dashboard')
                    #
                    # messages.error(request, "Your registration successfully")
                    # return redirect('login')

        else:
            messages.error(request, "password doesn't match")
            return redirect('registration')
    else:
        return render(request, 'accounts/registration.html')


@login_required(login_url='login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-created_date').filter(user_id=request.user.id)
    data = {
        'inquiry': user_inquiry
    }
    return render(request, 'accounts/dashboard.html', context=data)


def logout(request):
    auth.logout(request)
    return redirect('home')
