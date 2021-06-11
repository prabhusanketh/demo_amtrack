from django.shortcuts import render
import sys

from subprocess import run, PIPE


def button(request):
    return render(request, "home.html")


def external(request):
    inp = request.POST.get('param')
    out = run([sys.executable, 'C://Users//Prabh//PycharmProjects//AmTrack//buttons//buttons//fallan.py', inp], shell=False, stdout=PIPE)
    print(out)
    return render(request, 'home.html', {'data1': out.stdout})
