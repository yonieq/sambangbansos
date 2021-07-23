from django.urls import path

from .views import dashboard, daftar_usulan, pengajuan_check, ajukan_usulan_bst, ajukan_usulan_dd, let_usulan

urlpatterns = [
    path('', dashboard, name="UsulanDashboard"),
    path('pengajuan/nikcheck/', let_usulan, name="UsulanPengajuanForm"),
    path('pengajuan/bst/<slug:kode>/', ajukan_usulan_bst, name="UsulanPengajuanPenerimaBst"),
    path('pengajuan/dd/<slug:kode>/', ajukan_usulan_dd, name="UsulanPengajuanPenerimaDd"),
    path('list/', daftar_usulan, name="UsulanList"),
]
