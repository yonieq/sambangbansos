from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Database.models import Keluarga, Warga, PenerimaBantuan, UserDesa
from .forms import BantuanForms


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


@login_required(login_url='/management/')
def pencarian(request):
    user = UserDesa.objects.get(Username=request.user)
    if request.method == 'POST':
        nomer = request.POST['nomer']
        searchby = request.POST['searchby']
        data = None
        if searchby == 'nbykk':
            keluargaquery = Keluarga.objects.filter(NomerKK=nomer, Desa=user.Desa).first()
            if keluargaquery is not None:
                data = PenerimaBantuan.objects.filter(Keluarga=keluargaquery)
        elif searchby == 'bynik':
            wargaquery = Warga.objects.filter(Nik=nomer, Desa=user.Desa).first()
            if wargaquery is not None:
                data = PenerimaBantuan.objects.filter(Keluarga=wargaquery.Keluarga)

        return render(request, 'management/data/pencarian.html', {'list': data})
    else:
        return render(request, 'management/data/pencarian.html', {'list': None})


@login_required(login_url='/management/')
def bantuan_penerima(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Status='disetujui', Desa=user.Desa)

    return render(request, 'management/data/penerimabantuan.html', {'list': data})


@login_required(login_url='/management/')
def bantuan_detail(request, kode=None):
    data = PenerimaBantuan.objects.filter(Keluarga_id=kode)

    return render(request, 'management/data/detailbantuan.html', {'list': data})


@login_required(login_url='/management/')
def bantuan_forms(request, kode=None):
    # if request.method == 'POST':
    #     form = BantuanForms(request.POST)
    #     # if form.is_valid():
    #     # form.save()
    #     return redirect('DataBantuanPenerima')
    # else:
    #     form = BantuanForms
    #     return render(request, 'management/data/bantuanforms.html', {'form': form})
    if request.method == 'POST':
        form = BantuanForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bantuan = data['Bantuan']
            keluarga = data['Keluarga']
            status = data['Status']
            tglpengajuan = data['TglPengajuan']

            penerima_bantuans = PenerimaBantuan(Bantuan=bantuan, Keluarga=keluarga, Status=status, TglPengajuan=tglpengajuan)
            penerima_bantuans.save()
            return redirect('DataBantuanPenerima')
        else:
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = BantuanForms()

    return render(request, 'management/data/bantuanforms.html', {'form': form})


@login_required(login_url='/management/')
def bantuan_delete(request, kode=None):
    user = UserDesa.objects.get(Username=request.user)
    data_bantuan = PenerimaBantuan.objects.filter(pk=kode, Keluarga__Desa=user.Desa)
    for bantuan in data_bantuan:
        keluarga_id = bantuan.Keluarga_id
        bantuan.delete()
    return redirect('DataBantuanDetailList', keluarga_id)
