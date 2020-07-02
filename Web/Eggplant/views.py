from django.shortcuts import render, redirect
from Eggplant.models import User
from hashlib import md5
import time
from django.http import HttpResponse
def index(request):
    return render(request, "index.html")


def registration(request):
    data = {}
    if request.method == 'POST':
        if 'login' in request.POST and 'password' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            if len(User.objects.filter(login=login)) < 1:
                u = User(len(User.objects.all()) - 1, login, password)
                u.save()
                r = redirect("/login/")
                r.set_cookie(key="login", value=login, max_age=60000)
                return r

    return render(request, "registration.html", data)
def login(request):
    data = {}
    if 'login' in request.COOKIES:
        data['login'] = request.COOKIES['login']
    if request.method == 'POST':
        if 'login' in request.POST and 'password' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            if len(User.objects.filter(login=login, password=password)) == 1:
                r = redirect("/login/")
                m = md5()
                m.update((login + password + str(time.time())).encode())
                r.set_cookie(key="session", value=m.hexdigest(), max_age=60000)
                return r

    return render(request, "login.html", data)


def calc(request):
    w = 'err'
    a = 0
    b = 0
    if request.method == "GET":
        if "a" in request.GET and "b" in request.GET and "w" in request.GET:
            a = int(request.GET['a'])
            b = int(request.GET['b'])
            w = request.GET['w']
    elif request.method == "POST":
        if "a" in request.POST and "b" in request.POST and "w" in request.POST:
            a = int(request.POST['a'])
            b = int(request.POST['b'])
            w = request.POST['w']
    if w == '/':
        if b == 0:
            result = 'inf'
        else:
            result = a / b
    elif w == '*':
        result = a * b
    elif w == '+':
        result = a + b
    elif w == '-':
        result = a - b
    elif w == '%':
        if b == 0:
            result = 'inf'
        else:
            result = a % b
    elif w == '^' or w == '**':
        result = a ** b
    elif w == 'xor':
        result = a ^ b
    else:
        result = 'err'
    return render(request, "calc.html", {'result': result, 'a': a, "b": b, "w": w})
