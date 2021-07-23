from django.urls import path, include

from .views import index, data_warga_kecamatan, data_warga_desa, data_warga_aktif, data_aktif_download

urlpatterns = [
    path('', index, name="KabupatenInvalidIndex"),
    path('kecamatan/', data_warga_kecamatan, name="KabupatenDataKecamatan"),
    path('desa/', data_warga_desa, name='KabupatenDataDesa'),
    path('aktif/', data_warga_aktif, name='KabupatenDataAktif'),
    path('aktif/download/<slug:kode>/', data_aktif_download, name='KabupatenDataAktifDownload'),
]