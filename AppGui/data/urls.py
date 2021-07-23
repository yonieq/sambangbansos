from django.urls import path

from .views import dashboard, pencarian, bantuan_penerima, bantuan_detail, bantuan_forms, bantuan_delete

urlpatterns = [
    path('', dashboard, name="DataDashboard"),
    path('pencarian/', pencarian, name='DataBantuanPencarian'),
    path('penerimabantuan/list/', bantuan_penerima, name='DataBantuanPenerima'),
    path('penerimabantuan/detail/<slug:kode>/', bantuan_detail, name='DataBantuanDetailList'),
    path('penerimabantuan/forms/', bantuan_forms, name='DataBantuanDetailForm'),
    path('penerimabantuan/delete/<slug:kode>/', bantuan_delete, name='DataBantuanDetailDelete'),
]
