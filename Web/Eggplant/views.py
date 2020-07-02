from django.shortcuts import render


def index(request):
    return render(request, "index.html", {'a': 123})


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
    result = 0
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
