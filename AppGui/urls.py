from django.urls import path, include

from .views import index, do_login, do_logout, dashboard

urlpatterns = [
    path('', index, name="ManagementIndex"),
    path('login/', do_login, name='ManagementLogin'),
    path('logout/', do_logout, name='ManagementLogout'),
    path('dashboard/', dashboard, name="ManagementDashboard"),
    path('data/', include('AppGui.data.urls')),
    path('master/', include('AppGui.master.urls')),
    path('kependudukan/', include('AppGui.kependudukan.urls')),
    path('report/', include('AppGui.report.urls')),
    path('usulan/', include('AppGui.usulan.urls')),
    path('account/', include('AppGui.account.urls')),
]
