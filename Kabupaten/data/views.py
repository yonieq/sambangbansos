from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Database.models import Warga, Keluarga, Kecamatan, Desa, PenerimaBantuan


# Create your views here.
def cek_bantuan(list_data, keluarga, bantuan):
    for data in list_data:
        if data["Bantuan_id"] == bantuan and data["Keluarga_id"] == keluarga:
            return "TRUE"
    return "FALSE"


@login_required(login_url='KabupatenIndex')
@staff_member_required
def index(request):
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


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_warga_kecamatan(request):
    obj_kecamatan = Kecamatan.objects.order_by('Nama')
    list_data = []
    counter = 1
    for kecamatan in obj_kecamatan:
        data_invalid = Warga.objects.filter(NikValid=False, Desa__Kecamatan=kecamatan)
        data_valid = Warga.objects.filter(NikValid=True, Desa__Kecamatan=kecamatan)
        data = {
            "No": counter,
            "Kode": kecamatan.Kode,
            "Nama": kecamatan.Nama,
            "Invalid": data_invalid.count(),
            "Valid": data_valid.count(),
            "Total": data_invalid.count() + data_valid.count()
        }
        list_data.append(data)
        counter += 1

    return render(request, 'kabupaten/data/kecamatanlist.html', {'list': list_data})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_warga_desa(request):
    obj_desa = Desa.objects.order_by('Kecamatan__Nama', 'Kode')
    list_data = []
    counter = 1
    for desa in obj_desa:
        data_invalid = Warga.objects.filter(NikValid=False, Desa=desa)
        data_valid = Warga.objects.filter(NikValid=True, Desa=desa)
        data = {
            "No": counter,
            "Kode": desa.Kode,
            "Nama": desa.Nama,
            "Kecamatan": desa.Kecamatan.Nama,
            "Invalid": data_invalid.count(),
            "Valid": data_valid.count(),
            "Total": data_invalid.count() + data_valid.count()
        }
        list_data.append(data)
        counter += 1

    return render(request, 'kabupaten/data/desalist.html', {'list': list_data})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_warga_aktif(request):
    obj_desa = Desa.objects.order_by('Kecamatan__Nama', 'Kode')
    list_data = []
    counter = 1
    for desa in obj_desa:
        data_invalid = Warga.objects.filter(NikValid=False, Desa=desa)
        data_valid = Warga.objects.filter(NikValid=True, Desa=desa)
        data = {
            "No": counter,
            "Id": desa.id,
            "Kode": desa.Kode,
            "Nama": desa.Nama,
            "Kecamatan": desa.Kecamatan.Nama,
            "Invalid": data_invalid.count(),
            "Valid": data_valid.count(),
            "Total": data_invalid.count() + data_valid.count()
        }
        list_data.append(data)
        counter += 1

    return render(request, 'kabupaten/data/dataaktif.html', {'list': list_data})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_aktif_download(request, kode):
    obj_penerima_bantuan = PenerimaBantuan.objects.filter(Status=1, Keluarga__Desa__id=kode).values()
    obj_warga = Warga.objects.filter(NikValid=True, Desa__id=kode)
    list_data = []
    counter = 1
    for warga in obj_warga:
        data = {
            "No": counter,
            "Nik": "'" + warga.Nik,
            "Nama": warga.Nama,
            "TglLahir": warga.TglLahir,
            "Rt": warga.Rt,
            "Rw": warga.Rw,
            "BPNT": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 2),
        }
        list_data.append(data)
        counter += 1

    return render(request, 'kabupaten/data/aktifdownload.html', {'list': list_data})
