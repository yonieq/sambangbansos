from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime

from AppLogic.capil import check_nik
from AppLogic.keluarga import get_keluarga
from AppLogic.desa import get_desa
from Database.models import UserDesa, PenerimaBantuan, Warga, WARGA_STATUS


def add_penerima_bantuan(kode=None, bantuan_id=0):
    if kode is not None:
        warga = check_nik(kode)
        if warga is not None:
            nik = warga['NIK']
            nama = warga['NAMA_LGKP']
            tmplahir = warga['TMPT_LHR']
            tgllahir = warga['TGL_LHR']
            alamat = warga['ALAMAT']
            rt = warga['NO_RT']
            rw = warga['NO_RW']
            desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
            nokk = warga['NO_KK']
            keluarga = get_keluarga(nokk, warga)

            penerima = PenerimaBantuan.objects.filter(Keluarga=keluarga)
            if penerima.count() <= 0:
                existing = Warga.objects.filter(Nik=nik)
                if existing.count() <= 0:
                    obj_warga = Warga(Nik=nik, Nama=nama, TmpLahir=tmplahir, TglLahir=tgllahir, Alamat=alamat,
                                      Rt=rt, Rw=rw, NikValid=True, Desa=get_desa(desa),
                                      Keluarga=keluarga)
                    obj_warga.save()

                now = datetime.now()
                obj_penerima = PenerimaBantuan(Keluarga=keluarga, Bantuan_id=bantuan_id, Status=0,
                                               TglPengajuan=now.strftime("%Y-%m-%d"))
                obj_penerima.save()


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


@login_required(login_url='/management/')
def pengajuan_check(request):
    if request.method == 'POST':
        user = UserDesa.objects.get(Username=request.user)
        nomer = request.POST['nomer']

        list_data = []
        warga = check_nik(nomer)
        if warga is not None:
            desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
            if desa == user.Desa.Kode:
                nokk = warga['NO_KK']
                keluarga = get_keluarga(nomerkk=nokk, jsondata=warga)
                penerima = PenerimaBantuan.objects.filter(Keluarga=keluarga)

                data = {
                    "Nik": warga['NIK'],
                    "Nama": warga['NAMA_LGKP'],
                    "Alamat": warga['ALAMAT'],
                    "Rt": warga['NO_RT'],
                    "Rw": warga['NO_RW'],
                    "Menerima": penerima.count() > 0
                }
                list_data.append(data)

            return render(request, 'management/usulan/pengusulan.html', {'list': list_data})
        else:
            return render(request, 'management/usulan/pengusulan.html', {'list': None})
    else:
        return render(request, 'management/usulan/pengusulan.html', {'list': None})


@login_required(login_url='/management/')
def ajukan_usulan_bst(request, kode=None):
    add_penerima_bantuan(kode=kode, bantuan_id=1)
    return redirect('UsulanPengajuanForm')


@login_required(login_url='/management/')
def ajukan_usulan_dd(request, kode=None):
    add_penerima_bantuan(kode=kode, bantuan_id=2)
    return redirect('UsulanPengajuanForm')


@login_required(login_url='/management/')
def daftar_usulan(request):
    user = UserDesa.objects.get(Username=request.user)
    # penerima = PenerimaBantuan.objects.filter(Status=0, Keluarga__Desa=user.Desa)
    data = Warga.objects.filter(Desa=user.Desa, NikValid=True)

    return render(request, 'management/usulan/daftarusulan.html', {'list': data})


@login_required(login_url='/management/')
def let_usulan(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Status='usulan', Desa=user.Desa, NikValid=True)

    return render(request, 'management/usulan/pengusulan.html', {'list': data})
