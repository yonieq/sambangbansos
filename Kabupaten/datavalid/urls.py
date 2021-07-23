from django.urls import path, include

from .views import data_aktif_desa

urlpatterns = [
    path('aktif/', data_aktif_desa, name='KabupatenDataAktif'),
]