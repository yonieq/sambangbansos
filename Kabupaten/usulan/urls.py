from django.urls import path

from .views import index, data_usulan_all, data_usulan_desa, data_usulan_setuju

urlpatterns = [
    path('', index, name="KabupatenUsulanDashboard"),
    path('persetujuan/list/all', data_usulan_all, name="KabupatenUsulanListAll"),
    path('persetujuan/list/desa/<slug:kode>/', data_usulan_desa, name="KabupatenUsulanListDesa"),
    path('persetujuan/setuju/<slug:kode>/', data_usulan_setuju, name="KabupatenUsulanSetuju"),
]
