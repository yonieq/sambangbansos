from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Database.models import Warga, Desa


@login_required(login_url='KabupatenIndex')
@staff_member_required
def data_aktif_desa(request):
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

    return render(request, 'kabupaten/datainvalid/desalist.html', {'list': list_data})
