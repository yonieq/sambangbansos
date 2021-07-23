import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from AppLogic.capil import check_nik
from AppLogic.desa import get_desa
from AppLogic.keluarga import get_keluarga
from Database.models import Keluarga, Warga, UserDesa, StatusNonAktif
from .forms import KeluargaForms, WargaForms, RevisiNikForms, NonAktifStatusForms, KeluargaFormsUpdate, WargaFormsUpdate
from django.contrib import messages

logger = logging.getLogger(__name__)


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


@login_required(login_url='/management/')
def warga_list(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Desa=user.Desa, NikValid=True)

    return render(request, 'management/kependudukan/wargalist.html', {'list': data})


@login_required(login_url='/management/')
def warga_forms(request):
    if request.method == 'POST':
        form = WargaForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nik = data['Nik']
            nama = data['Nama']
            tmptlahir = data['TmptLahir']
            tgllahir = data['TglLahir']
            alamat = data['Alamat']
            rt = data['Rt']
            rw = data['Rw']
            desa = data['Desa']
            keluarga = data['Keluarga']
            nikvalid = data['NikValid']

            wargas = Warga(Nik=nik, Nama=nama, TmpLahir=tmptlahir, TglLahir=datetime.now().strftime("%Y-%m-%d"),
                           Alamat=alamat, Rt=rt, Rw=rw, Desa=desa, Keluarga=keluarga, NikValid=nikvalid)
            wargas.save()
            messages.success(request, 'Data Berhasil Ditambah!')
            return redirect('KependudukanWargaList')
        else:
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = WargaForms()

    return render(request, 'management/kependudukan/wargaforms.html', {'form': form})


@login_required(login_url='/management/')
def warga_delete(request, kode=None):
    warga = Warga.objects.get(Nik=kode)
    warga.NikValid = False
    warga.save()
    warga.delete()
    return redirect('KependudukanWargaList')

@login_required(login_url='/management/')
def warga_update(request, kode=None):
    wargas_update = Warga.objects.get(pk=kode)
    data = {
        'nik': wargas_update.Nik,
        'nama': wargas_update.Nama,
        'tmptlahir': wargas_update.TglLahir,
        'tgllahir': wargas_update.TglLahir,
        'alamat': wargas_update.Alamat,
        'rt': wargas_update.Rt,
        'rw': wargas_update.Rw,
        'desa': wargas_update.Desa,
        'keluarga': wargas_update.Keluarga,
        'nikvalid': wargas_update.NikValid,
    }
    form = WargaFormsUpdate(request.POST or None, initial=data, instance=wargas_update)

    if request.method == 'POST':
        if form.is_valid():

            form.save()
            messages.success(request, 'Data Berhasil Diubah!')
            return redirect('KependudukanWargaList')
        else:
            print(form.errors)

    return render(request, 'management/kependudukan/wargaforms.html', {'form': form})



@login_required(login_url='/management/')
def keluarga_list(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Keluarga.objects.filter(Desa=user.Desa)

    return render(request, 'management/kependudukan/keluargalist.html', {'list': data})


@login_required(login_url='/management/')
def keluarga_forms(request):
    if request.method == 'POST':
        form = KeluargaForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nomerKK = data['NomerKK']
            alamat = data['Alamat']
            rt = data['Rt']
            rw = data['Rw']
            desa = data['Desa']

            keluargas = Keluarga(NomerKK=nomerKK, Alamat=alamat, Rt=rt, Rw=rw, Desa=desa)
            keluargas.save()
            messages.success(request, 'Data Berhasil Ditambah!')
            return redirect('KependudukanKeluargaList')
        else:
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = KeluargaForms()

    return render(request, 'management/kependudukan/keluargaforms.html', {'form': form})

@login_required(login_url='/management/')
def keluarga_delete(request, kode=None):
    keluarga = Keluarga.objects.get(pk=kode)
    keluarga.delete()
    return redirect('KependudukanKeluargaList')

@login_required(login_url='/management/')
def keluarga_update(request, kode=None):
    keluargas_update = Keluarga.objects.get(pk=kode)
    data = {
        'nomerKK'   : keluargas_update.NomerKK,
        'alamat'    : keluargas_update.Alamat,
        'rt'        : keluargas_update.Rt,
        'rw'        : keluargas_update.Rw,
        'desa'      : keluargas_update.Desa,
    }
    form = KeluargaFormsUpdate(request.POST or None, initial=data, instance=keluargas_update)

    if request.method == 'POST':
        # keluargaupdate_forms = KeluargaFormsUpdate(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            # nomerKK = data['NomerKK']
            # alamat = data['Alamat']
            # rt = data['Rt']
            # rw = data['Rw']
            # desa = data['Desa']
            #
            # keluargas = Keluarga(NomerKK=nomerKK, Alamat=alamat, Rt=rt, Rw=rw, Desa=desa)
            messages.success(request, 'Data Berhasil Diubah!')
            form.save()
            return redirect('KependudukanKeluargaList')
        else:
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    # else:
    #     keluargaupdate_forms = KeluargaFormsUpdate()

    return render(request, 'management/kependudukan/keluargaforms.html', {'form': form})


@login_required(login_url='/management/')
def invalid_warga(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Desa=user.Desa, NikValid=False)
    return render(request, 'management/kependudukan/invalidwargalist.html', {'list': data})


@login_required(login_url='/management/')
def revisi_nik_forms(request, kode=None):
    if request.method == 'POST':
        db_object = Warga.objects.get(pk=kode)
        form = RevisiNikForms(request.POST, instance=db_object)
        if form.is_valid():
            form.save()

        warga = check_nik(db_object.Nik)
        if warga is not None:
            desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
            nokk = warga['NO_KK']
            db_object.Nik = warga['NIK']
            db_object.Nama = warga['NAMA_LGKP']
            db_object.TmpLahir = warga['TMPT_LHR']
            db_object.TglLahir = warga['TGL_LHR']
            db_object.Alamat = warga['ALAMAT']
            db_object.Rt = warga['NO_RT']
            db_object.Rw = warga['NO_RW']
            db_object.NikValid = False
            # db_object.Keluarga = update_keluarga(db_object.Keluarga, warga)
            db_object.Keluarga = get_keluarga(nomerkk=nokk, jsondata=warga)
            db_object.Desa = get_desa(desa)
            db_object.save()

        return redirect('KependudukanInvalidWargaList')
    else:
        if kode is not None:
            db_object = Warga.objects.get(pk=kode)
            warga = check_nik(db_object.Nik)
            if warga is not None:
                desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
                nokk = warga['NO_KK']
                nik = warga['NIK']
                nama = warga['NAMA_LGKP']
                tmplahir = warga['TMPT_LHR']
                tgllahir = warga['TGL_LHR']
                alamat = warga['ALAMAT']
                rt = warga['NO_RT']
                rw = warga['NO_RW']
                # keluarga = update_keluarga(db_object.Keluarga, warga)
                keluarga = get_keluarga(nomerkk=nokk, jsondata=warga)

                obj_warga = Warga(Nik=nik, Nama=nama, TmpLahir=tmplahir, TglLahir=tgllahir, Alamat=alamat,
                                  Rt=rt, Rw=rw, NikValid=True, Desa=get_desa(desa),
                                  Keluarga=keluarga)

                form = RevisiNikForms(instance=obj_warga)
            else:
                form = RevisiNikForms(instance=db_object)
        else:
            form = RevisiNikForms
        return render(request, 'management/kependudukan/revisinikforms.html', {'form': form})


@login_required(login_url='/management/')
def check_invalid_warga(request, kode=None):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Desa=user.Desa, NikValid=False)
    if kode is not None:
        db_object = Warga.objects.get(pk=kode)
        warga = check_nik(db_object.Nik)
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

            existing = Warga.objects.get(pk=kode)
            existing.Nik = nik
            existing.Nama = nama
            existing.TmpLahir = tmplahir
            existing.TglLahir = tgllahir
            existing.Alamat = alamat
            existing.Rt = rt
            existing.Rw = rw
            existing.Desa = get_desa(desa)
            # existing.Keluarga = update_keluarga(existing.Keluarga, warga)
            existing.Keluarga = get_keluarga(nomerkk=nokk, jsondata=warga)
            existing.NikValid = True
            existing.save()
        else:
            logger.error("Can't connect to Ducapil server")
    else:
        logger.error("Warga primary key not found")

    return render(request, 'management/kependudukan/invalidwargalist.html', {'list': data})


@login_required(login_url='/management/')
def check_nik_warga(request, kode=None):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Desa=user.Desa)

    return render(request, 'management/kependudukan/checknikwarga.html', {'list': data})
    # if request.method == 'POST':
    #     user = UserDesa.objects.get(Username=request.user)
    #     nomer = request.POST['nomer']
    #
    #     list_data = []
    #     warga = check_nik(nomer)
    #     if warga is not None:
    #         desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
    #         if desa == user.Desa.Kode:
    #             data = {
    #                 "Nik": warga['NIK'],
    #                 "Nama": warga['NAMA_LGKP'],
    #                 "Alamat": warga['ALAMAT'],
    #                 "Rt": warga['NO_RT'],
    #                 "Rw": warga['NO_RW'],
    #             }
    #             list_data.append(data)
    #
    #         return render(request, 'management/kependudukan/checknikwarga.html', {'list': list_data})
    #     else:
    #         return render(request, 'management/kependudukan/checknikwarga.html', {'list': None})
    # else:
    #     return render(request, 'management/kependudukan/checknikwarga.html', {'list': None})



@login_required(login_url='/management/')
def non_aktif_status(request, kode=None):
    if request.method == 'POST':

        forms = NonAktifStatusForms(request.POST)
        if forms.is_valid():
            warga = Warga.objects.get(id=kode)
            datas = forms.cleaned_data

            existing = StatusNonAktif.objects.filter(Warga__id=kode)
            if existing.count() > 0:
                status = existing.first()
                status.Status = datas['Status']
                status.UpdateDate=datetime.now().strftime("%Y-%m-%d")
                status.save()
                print(existing.count())
            else:
                status = StatusNonAktif(Warga=warga, Status=datas['Status'],
                                        UpdateDate=datetime.now().strftime("%Y-%m-%d"))
                status.save()

        return render(request, 'management/kependudukan/nonaktifstatus.html', {'form': forms})
    else:
        warga = Warga.objects.get(id=kode)
        data = {
            "Nik": warga.Nik,
            "Nama": warga.Nama,
            "Alamat": warga.Alamat,
        }
        forms = NonAktifStatusForms(initial=data)
        return render(request, 'management/kependudukan/nonaktifstatus.html', {'form': forms})
