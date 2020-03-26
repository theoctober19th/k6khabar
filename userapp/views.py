from django.shortcuts import render


def loginview(request):
    return render(request, 'userapp/login.html')
