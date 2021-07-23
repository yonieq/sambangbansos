from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Database.models import Kecamatan, Desa, Bantuan


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


@login_required(login_url='/management/')
def bantuan(request):
    data = Bantuan.objects.all()

    return render(request, 'management/master/bantuan.html', {'list': data})


@login_required(login_url='/management/')
def desa(request):
    data = Desa.objects.all()

    return render(request, 'management/master/desa.html', {'list': data})


@login_required(login_url='/management/')
def kecamatan(request):
    data = Kecamatan.objects.all()

    return render(request, 'management/master/kecamatan.html', {'list': data})
