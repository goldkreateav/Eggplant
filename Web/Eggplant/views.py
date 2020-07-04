from django.shortcuts import render, redirect
from Eggplant.models import User, Session, Order
from hashlib import md5
import time


def index(request):
    data = {}
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            data['authorized'] = True
    return render(request, "index.html", data)


def printr(request):
    data = {}
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            username=Session.objects.filter(cookie=request.COOKIES['session'])[0].uid
            data['authorized'] = True
            if request.method == 'POST':
                if 'list' in request.POST and 'color' in request.POST and 'where' in request.POST and \
                        'file' in request.FILES:
                    file = request.FILES['file']
                    fname = md5((file.name + username).encode()).hexdigest()
                    open('uploads/' + fname, 'bw+').write(file.read())
                    o = Order(file=fname, client=username, provider=request.POST['where'])
                    o.save()
                    data['ok'] = True
            return render(request, "print.html", data)
    return redirect('/')


def registration(request):
    data = {}
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            return redirect('/account/')
    if request.method == 'POST':
        if 'login' in request.POST and 'password' in request.POST and 'type' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            type = request.POST['type']
            if len(User.objects.filter(login=login)) < 1:
                u = User(len(User.objects.all()) - 1, login, password, type, 2)#len(User.objects.filter(type=1)) - 1)
                u.save()
                r = redirect("/login/")
                r.set_cookie(key="login", value=login, max_age=60000)
                return r

    return render(request, "registration.html", data)


def login(request):
    data = {}
    if 'login' in request.COOKIES:
        data['login'] = request.COOKIES['login']
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            return redirect('/account/')
    if request.method == 'POST':
        if 'login' in request.POST and 'password' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            if len(User.objects.filter(login=login, password=password)) == 1:
                r = redirect("/account/")
                m = md5()

                m.update((login + password + str(time.time())).encode())
                s = m.hexdigest()
                n = Session(cookie=s, uid=User.objects.filter(login=login)[0].login)
                n.save()
                r.set_cookie(key="session", value=s, max_age=60000)
                return r
    return render(request, "login.html", data)


def account(request):
    data = {}
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            data['authorized'] = True
            login = Session.objects.filter(cookie=request.COOKIES['session'])[0].uid
            data['type'] = User.objects.filter(login=login)[0].type
            return render(request, "account.html", data)
    return redirect('/')


def orders(request):
    data = {}
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            data['authorized'] = True
            user = User.objects.filter(login=Session.objects.filter(cookie=request.COOKIES['session'])[0].uid)[0]
            if user.type == 2:
                return redirect('/account/')
            data['orders'] = [i for i in Order.objects.filter(provider=user.pid)]
            return render(request, "orders.html", data)
    return redirect('/')


def exit(request):
    if 'session' in request.COOKIES:
        if len(Session.objects.filter(cookie=request.COOKIES['session'])) == 1:
            d = Session.objects.filter(cookie=request.COOKIES['session'])[0]
            d.delete()
    return redirect('/')


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
