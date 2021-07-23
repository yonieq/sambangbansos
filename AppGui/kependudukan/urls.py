from django.urls import path

from .views import dashboard, keluarga_list, keluarga_forms, keluarga_delete, warga_list, warga_forms, warga_delete, \
    invalid_warga, revisi_nik_forms, check_invalid_warga, check_nik_warga, non_aktif_status, keluarga_update, warga_update

urlpatterns = [
    path('', dashboard, name="KependudukanDashboard"),
    path('checknik/', check_nik_warga, name='KependudukanCheckNikWarga'),
    path('warga/list/', warga_list, name='KependudukanWargaList'),
    path('warga/forms/', warga_forms, name='KependudukanWargaFormsInsert'),
    path('warga/forms/update/<slug:kode>/', warga_update, name='KependudukanWargaFormsUpdate'),
    path('warga/delete/<slug:kode>/', warga_delete, name='KependudukanWargaDelete'),
    path('keluarga/list/', keluarga_list, name='KependudukanKeluargaList'),
    path('keluarga/forms/', keluarga_forms, name='KependudukanKeluargaFormsInsert'),
    path('keluarga/forms/update/<slug:kode>/', keluarga_update, name='KependudukanKeluargaFormsUpdate'),
    path('keluarga/delete/<slug:kode>/', keluarga_delete, name='KependudukanKeluargaDelete'),
    path('invalid/warga/list/', invalid_warga, name='KependudukanInvalidWargaList'),
    path('invalid/warga/revisi/', revisi_nik_forms, name='KependudukanInvalidWargaRevisiSearch'),
    path('invalid/warga/revisi/<slug:kode>/', revisi_nik_forms, name='KependudukanInvalidWargaRevisi'),
    path('invalid/warga/check/<slug:kode>/', check_invalid_warga, name='KependudukanInvalidWargaCheck'),
    path('invalid/warga/status/<slug:kode>/', non_aktif_status, name='KependudukanInvalidNonAktifStatus'),
]
