from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Database.models import Warga, Keluarga, Desa, PenerimaBantuan


# Create your views here.

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
def data_usulan_all(request):
    obj_desa = Desa.objects.order_by('Kecamatan__Nama', 'Kode')
    list_data = []
    counter = 1
    for desa in obj_desa:
        usulan = Warga.objects.filter(Status='usulan', Keluarga__Desa=desa)
        data = {
            "No": counter,
            "Id": desa.id,
            "Kode": desa.Kode,
            "Nama": desa.Nama,
            "Kecamatan": desa.Kecamatan.Nama,
            "Usulan": usulan.count(),
        }
        list_data.append(data)
        counter += 1

    return render(request, 'kabupaten/usulan/daftarusulan.html', {'list': list_data})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_usulan_desa(request, kode=None):
    usulan = Warga.objects.filter(Status='usulan', Keluarga__Desa_id=kode)

    return render(request, 'kabupaten/usulan/detailusulan.html', {'list': usulan})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_usulan_setuju(request, kode=None):
    usulan = Warga.objects.get(pk=kode)
    usulan.Status = 'disetujui'
    usulan.save()
    desa_id = usulan.Keluarga.Desa.id

    return redirect('KabupatenUsulanListDesa', desa_id)
