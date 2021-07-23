from django.urls import path

from .views import dashboard, penerima_bantuan_list, excel_format

urlpatterns = [
    path('', dashboard, name="ReportDashboard"),
    path('penerimabantuan/', penerima_bantuan_list, name="ReportPenerimaBantuanList"),
    path('excelformat/', excel_format, name="ReportExcelFormat"),
]
