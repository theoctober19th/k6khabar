from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserModel


def loginview(request):
    return render(request, 'userapp/login.html')


def registerview(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        status = request.POST.get('status')
        profile_pic = request.POST.get('profilepic')

        user = User(username=username, password=password, email=email,
                    first_name=fname, last_name=lname, is_active=True)
        user.save()
        usermodel = UserModel(auth=user, status=status,
                              profile_picture=profile_pic)
        usermodel.save()
        return redirect('index')
    else:
        return render(request, 'userapp/register.html')
