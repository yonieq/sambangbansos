from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as views_token

from .views import KecamatanViewSet, DesaViewSet, BantuanViewSet, UserViewSet, WargaViewSet, KeluargaViewSet, CustomAuthToken, UsulanViewSet, PenerimaBantuanViewSet
from .views import penerima, create_user, check_nik_exist

router = routers.DefaultRouter()
router.register(r'usulan', UsulanViewSet)
router.register(r'penerimabantuan', PenerimaBantuanViewSet)
router.register(r'warga', WargaViewSet)
router.register(r'keluarga', KeluargaViewSet)
router.register(r'bantuan', BantuanViewSet)
router.register(r'desa', DesaViewSet)
router.register(r'kecamatan', KecamatanViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls), name='RestApi'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('penerima/', penerima, name='Penerima'),
    # path('auth/', views_token.obtain_auth_token, name='api_auth_token'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('createuser/', create_user, name='CreateUser'),
    path('checknik/', check_nik_exist, name='CheckNik'),
]
