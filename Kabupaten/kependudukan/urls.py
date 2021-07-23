from django.urls import path

from .views import index, warga_forms

urlpatterns = [
    path('warga/edit/list/', index, name="KabupatenKependudukanWargaList"),
    path('warga/edit/forms/<slug:kode>/', warga_forms, name='KabupatenKependudukanWargaFormsUpdate'),
]
