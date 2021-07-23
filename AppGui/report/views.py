import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from AppLogic.stringutil import replace_kk
from Database.models import Warga, Keluarga, UserDesa, PenerimaBantuan

logger = logging.getLogger(__name__)


def cek_bantuan(list_data, keluarga, bantuan):
    for data in list_data:
        if data["Bantuan_id"] == bantuan and data["Keluarga_id"] == keluarga:
            return "TRUE"
    return "FALSE"


def get_keluarga(list_data, keluarga):
    for data in list_data:
        if data["id"] == keluarga:
            return data
    logger.error(keluarga)
    return None


def get_desa(list_data, desa):
    for data in list_data:
        if data["id"] == desa:
            return data
    return None


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


@login_required(login_url='/management/')
def penerima_bantuan_list(request):
    user = UserDesa.objects.get(Username=request.user)
    data = Warga.objects.filter(Status='disetujui', Desa=user.Desa, NikValid=True)

    return render(request, 'management/report/penerimabantuan.html', {'list': data})


@login_required(login_url='/management/')
def excel_format(request):
    user = UserDesa.objects.get(Username=request.user)
    obj_warga = Warga.objects.filter(Desa=user.Desa, NikValid=True, Status=1)
    obj_keluarga = Keluarga.objects.filter(Desa=user.Desa).values()
    obj_penerima_bantuan = PenerimaBantuan.objects.filter(Status=1, Keluarga__Desa=user.Desa).values()

    list_data = []
    counter = 1
    for warga in obj_warga:
        keluarga = get_keluarga(obj_keluarga, warga.Keluarga_id)
        if keluarga is not None:
            nomer_kk = keluarga["NomerKK"]
        else:
            nomer_kk = "0000000000000001"

        data = {
            "No": counter,
            "Nik": "'" + warga.Nik,
            #        "NomerKK": replace_kk(warga.Keluarga.NomerKK, 9, 2),
            "NomerKK": replace_kk(nomer_kk, 9, 4),
            "Nama": warga.Nama,
            "TmpLahir": warga.TmpLahir,
            "TglLahir": warga.TglLahir.strftime("%d/%m/%Y"),
            "Alamat": warga.Alamat,
            "Rt": warga.Rt,
            "Rw": warga.Rw,
            "KodeDesa": user.Desa.Kode,  # get_desa(obj_desa, warga.Desa_id)["Kode"],
            "PKH": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 1),
            "BPNT": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 2),
            "BSTP": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 3),
            "Sembako": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 4),
            "JPS": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 5),
            "BSTKab": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 6),
            "BltDd": cek_bantuan(obj_penerima_bantuan, warga.Keluarga_id, 7),
            #        "KodeDesa": warga.Desa.Kode,
            #        "KodeKecamatan": warga.Desa.Kecamatan.Kode,
            #        "PKH": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan_id=1).count() > 0,
            #        "BPNT": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=2).count() > 0,
            #        "BSTP": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=3).count() > 0,
            #        "Sembako": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=4).count() > 0,
            #        "JPS": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=5).count() > 0,
            #        "BSTKab": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=6).count() > 0,
            #        "BltDd": PenerimaBantuan.objects.filter(Keluarga=warga.Keluarga, Bantuan__id=7).count() > 0,

        }
        list_data.append(data)
        counter += 1

    return render(request, 'management/report/excelformat.html', {'list': list_data})
