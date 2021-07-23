from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Database.models import Warga, Keluarga


# Create your views here.
def index(request):
    return render(request, 'kabupaten/login.html')


def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        response = redirect('KabupatenDashboard')
    else:
        response = redirect('KabupatenIndex')
    return response


def do_logout(request):
    logout(request)
    response = redirect('KabupatenIndex')
    return response


@login_required(login_url='KabupatenIndex')
@staff_member_required
def dashboard(request):
    total = Warga.objects.all().count()
    valid = Warga.objects.filter(NikValid=True).count()
    invalid = total - valid
    keluarga = Keluarga.objects.all().count()
    persen_keluarga = (keluarga / total) * 100
    persen_valid = (valid / total) * 100
    persen_invalid = (invalid / total) * 100

    data = {
        "Total": total,
        "Valid": valid,
        "Invalid": invalid,
        "Keluarga": keluarga,
        "PersenKeluarga": str(persen_keluarga) + '%',
        "PersenValid": str(persen_valid) + '%',
        "PersenInvalid": str(persen_invalid) + '%',
    }

    # print(str(terverifikasi.count()) + " " + str(total.count()))
    return render(request, 'kabupaten/dashboard.html', {'data': data})
