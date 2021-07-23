from django.urls import path, include

from .views import index, do_login, do_logout, dashboard

urlpatterns = [
    path('', index, name="KabupatenIndex"),
    path('login/', do_login, name='KabupatenLogin'),
    path('logout/', do_logout, name='KabupatenLogout'),
    path('dashboard/', dashboard, name="KabupatenDashboard"),
    path('kependudukan/', include('Kabupaten.kependudukan.urls')),
    path('data/', include('Kabupaten.data.urls')),
    path('usulan/', include('Kabupaten.usulan.urls')),
]