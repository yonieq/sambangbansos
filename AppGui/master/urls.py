from django.urls import path

from .views import dashboard, kecamatan, desa, bantuan

urlpatterns = [
    path('', dashboard, name="MasterDashboard"),
    path('kecamatan/', kecamatan, name='MasterKecamatan'),
    path('desa/', desa, name='MasterDesa'),
    path('bantuan/', bantuan, name='MasterBantuan'),
]
