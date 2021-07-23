import json
import logging

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets, status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from AppLogic.capil import check_nik
from AppLogic.desa import get_desa
from AppLogic.keluarga import get_keluarga
from Database.models import Kecamatan, Desa, Bantuan, Keluarga, Warga, PenerimaBantuan, UserDesa
from .serializers import KecamatanSerializer, DesaSerializer, BantuanSerializer, KeluargaSerializer, UserSerializer, \
    WargaSerializer, PenerimaBantuanSerializer

logger = logging.getLogger(__name__)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': True,
            'message': 'Login successfully',
            'token': token.key,
            'user': {'user_id': user.pk, 'username': user.username, 'email': user.email}
        })


# Create your views here.
@csrf_exempt
def create_user(request):
    try:
        if request.method == 'POST':
            data = request.body

            status = "Ok"
            message = ""

            bodydata = json.loads(data.decode())

            username = bodydata["Username"]
            password = bodydata["Password"]
            email = bodydata["Email"]
            kodedesa = bodydata["KodeDesa"]

            if User.objects.filter(username=username).count() <= 0:
                user = User.objects.create_user(username, email, password)
                user.save()
            else:
                user = User.objects.get(username=username)

            group = Group.objects.get(name='Desa')
            group.user_set.add(user)
            desa = Desa.objects.get(Kode=kodedesa)
            if UserDesa.objects.filter(Username=username).count() <= 0:
                userdesa = UserDesa(Username=username, Desa=desa)
                userdesa.save()
                status = "Ok"
                message = "User Created"

            response = {
                "Status": status,
                "Message": message,
            }
            return JsonResponse(response)
    except Exception as e:
        logger.error(e)
        response = {
            "Status": "Error",
            "Message": e,
        }
        return JsonResponse(response)


@csrf_exempt
def penerima(request):
    try:
        if request.method == 'POST':
            data = request.body

            status = "Ok"
            message = ""

            bodydata = json.loads(data.decode())

            nik = bodydata["NIK"]
            nama = bodydata["NAMA_LGKP"]
            tmplahir = bodydata["TMPT_LHR"]
            tgllahir = bodydata["TGL_LHR"]
            alamat = bodydata["ALAMAT"]
            rt = bodydata["NO_RT"]
            rw = bodydata["NO_RW"]
            nokk = bodydata["NO_KK"]
            desa = str(bodydata['NO_KEC']).zfill(2) + '.' + str(bodydata['NO_KEL']) + '.'

            warga = check_nik(nik)
            if warga is not None:
                nik = warga['NIK']
                nama = warga['NAMA_LGKP']
                tmplahir = warga['TMPT_LHR']
                tgllahir = warga['TGL_LHR']
                alamat = warga['ALAMAT']
                rt = warga['NO_RT']
                rw = warga['NO_RW']
                desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
                nokk = warga['NO_KK']
                keluarga = get_keluarga(nokk, warga)

                existing = Warga.objects.filter(Nik=nik)
                if existing.count() <= 0:
                    obj_warga = Warga(Nik=nik, Nama=nama, TmpLahir=tmplahir, TglLahir=tgllahir, Alamat=alamat,
                                      Rt=rt, Rw=rw, NikValid=True, Desa=get_desa(desa),
                                      Keluarga=keluarga)
                    obj_warga.save()
                else:
                    datawarga = existing[0]
                    datawarga.Nik = nik
                    datawarga.Nama = nama
                    datawarga.TmpLahir = tmplahir
                    datawarga.TglLahir = tgllahir
                    datawarga.Alamat = alamat
                    datawarga.Rt = rt
                    datawarga.Rw = rw
                    datawarga.Desa = get_desa(desa)
                    datawarga.Keluarga = keluarga
                    datawarga.save()

                    status = "Warning"
                    message += "Double NIK, "
            else:
                keluarga = get_keluarga(nokk, bodydata)

                existing = Warga.objects.filter(Nik=nik)
                if existing.count() <= 0:
                    obj_warga = Warga(Nik=nik, Nama=nama, TmpLahir=tmplahir, TglLahir=tgllahir, Alamat=alamat,
                                      Rt=rt, Rw=rw, NikValid=False, Desa=get_desa(desa),
                                      Keluarga=keluarga)
                    obj_warga.save()
                else:
                    status = "Warning"
                    message += "Double NIK, "

            if bodydata["Bantuan1"]:
                bantuan = Bantuan.objects.get(id=1)
                databantuan1 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan1.count() <= 0:
                    bantuan1 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan1.save()

            if bodydata["Bantuan2"]:
                bantuan = Bantuan.objects.get(id=2)
                databantuan2 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan2.count() <= 0:
                    bantuan2 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan2.save()

            if bodydata["Bantuan3"]:
                bantuan = Bantuan.objects.get(id=3)
                databantuan3 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan3.count() <= 0:
                    bantuan3 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan3.save()

            if bodydata["Bantuan4"]:
                bantuan = Bantuan.objects.get(id=4)
                databantuan4 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan4.count() <= 0:
                    bantuan4 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan4.save()

            if bodydata["Bantuan5"]:
                bantuan = Bantuan.objects.get(id=5)
                databantuan5 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan5.count() <= 0:
                    bantuan5 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan5.save()

            if bodydata["Bantuan6"]:
                bantuan = Bantuan.objects.get(id=6)
                databantuan6 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan6.count() <= 0:
                    bantuan6 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan6.save()

            if bodydata["Bantuan7"]:
                bantuan = Bantuan.objects.get(id=7)
                databantuan7 = PenerimaBantuan.objects.filter(Keluarga=keluarga, Bantuan=bantuan)
                if databantuan7.count() <= 0:
                    bantuan7 = PenerimaBantuan(Keluarga=keluarga, Bantuan=bantuan)
                    bantuan7.save()

            response = {
                "Status": status,
                "Message": message,
            }
        else:
            response = {
                "Status": "Error",
                "Message": "Error, HTTP Method invalid",
            }

        return JsonResponse(response)
    except Exception as e:
        logger.error(e)
        response = {
            "Status": "Error",
            "Message": e,
        }
        return JsonResponse(response)


@csrf_exempt
def check_nik_exist(request):
    try:
        if request.method == 'POST':
            data = request.body
            bodydata = json.loads(data.decode())

            nik = bodydata["NIK"]
            # print(Warga.objects.filter(Nik=nik, NikValid=False).count())
            if Warga.objects.filter(Nik=nik, NikValid=False).count() <= 0:
                status = "Ok"
                message = "NIK Exist"
            else:
                warga = check_nik(nik)
                if warga is not None:
                    nik = warga['NIK']
                    nama = warga['NAMA_LGKP']
                    tmplahir = warga['TMPT_LHR']
                    tgllahir = warga['TGL_LHR']
                    alamat = warga['ALAMAT']
                    rt = warga['NO_RT']
                    rw = warga['NO_RW']
                    desa = str(warga['NO_KEC']).zfill(2) + '.' + str(warga['NO_KEL']) + '.'
                    nokk = warga['NO_KK']
                    keluarga = get_keluarga(nokk, warga)

                    existing = Warga.objects.filter(Nik=nik)
                    if existing.count() <= 0:
                        obj_warga = Warga(Nik=nik, Nama=nama, TmpLahir=tmplahir, TglLahir=tgllahir, Alamat=alamat,
                                          Rt=rt, Rw=rw, NikValid=True, Desa=get_desa(desa),
                                          Keluarga=keluarga)
                        obj_warga.save()
                    else:
                        datawarga = existing[0]
                        datawarga.Nik = nik
                        datawarga.Nama = nama
                        datawarga.TmpLahir = tmplahir
                        datawarga.TglLahir = tgllahir
                        datawarga.Alamat = alamat
                        datawarga.Rt = rt
                        datawarga.Rw = rw
                        datawarga.NikValid = True
                        datawarga.Desa = get_desa(desa)
                        datawarga.Keluarga = keluarga
                        datawarga.save()
                    status = "Ok"
                    message = "NIK Created"
                else:
                    status = "Error"
                    message = "Can't connect to dukcapil"
        else:
            status = "Error"
            message = "Error, HTTP Method invalid"

        response = {
            "Status": status,
            "Message": message,
        }
        return JsonResponse(response)

    except Exception as e:
        logger.error(e)
        response = {
            "Status": "Error",
            "Message": e,
        }
        return JsonResponse(response)


class KecamatanViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Kecamatan.objects.all()
    serializer_class = KecamatanSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        kecamatan = Kecamatan.objects.all()
        serializer = KecamatanSerializer(kecamatan, many=True)
        return Response({"status": True, "message": "Sukses !", "data_desa": serializer.data})


class DesaViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Desa.objects.all()
    serializer_class = DesaSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        desa = Desa.objects.all()
        serializer = DesaSerializer(desa, many=True)
        return Response({"status": True, "message": "Sukses !", "data_desa": serializer.data})


class BantuanViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Bantuan.objects.all()
    serializer_class = BantuanSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        bantuan = Bantuan.objects.all()
        serializer = BantuanSerializer(bantuan, many=True)
        return Response({"status": True, "message": "Sukses !", "data": serializer.data})


# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'status': True,
#             'message': 'Login successfully',
#             'token': token.key,
#             'user': {'user_id': user.pk, 'username': user.username, 'email': user.email}
#         })

class KeluargaViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Keluarga.objects.all()

    serializer_class = KeluargaSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = UserDesa.objects.get(Username=request.user)
        keluarga = Keluarga.objects.filter(Desa=user.Desa)
        serializer = KeluargaSerializer(keluarga, many=True)
        return Response({"status": True, "message": "Sukses !", "data_keluarga": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = UserDesa.objects.get(Username=request.user)
        keluarga = Keluarga.objects.filter(Desa=user.Desa)
        instance = self.get_object()
        serializer = self.get_serializer(keluarga, instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_object_cache', None):
            instance._prefetched_object_cache = {}

        return Response({"status": True, "message": "Data Telah Diubah", "data_keluarga": serializer.data})

    def create(self, request, *args, **kwargs):
        # user = UserDesa.objects.get(Username=request.user)
        # keluarga = Keluarga.objects.filter(Desa=user.Desa)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Status": True, "message": "Data Telah ditambah !", "data_keluarga": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Status": True, "message": "Data Telah dihapus !"})


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"status": True, "message": "Sukses !", "data": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Status": True, "message": "Data Telah ditambah !", "data": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class WargaViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Warga.objects.all()
    serializer_class = WargaSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = UserDesa.objects.get(Username=request.user)
        warga = Warga.objects.filter(Desa=user.Desa)
        # warga = Warga.objects.all()
        serializer = WargaSerializer(warga, many=True)
        return Response({"status": True, "message": "Sukses !", "data_warga": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Status": True, "message": "Data Telah ditambah !", "data_warga": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_object_cache', None):
            instance._prefetched_object_cache = {}

        return Response({"status": True, "message": "Data Telah Diubah", "data_warga": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Status": True, "message": "Data Telah dihapus !"})


class UsulanViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Warga.objects.all()
    serializer_class = WargaSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = UserDesa.objects.get(Username=request.user)
        warga = Warga.objects.filter(Desa=user.Desa)
        # warga = Warga.objects.all()
        serializer = WargaSerializer(warga, many=True)
        return Response({"status": True, "message": "Sukses !", "data_usulan_warga": serializer.data})


class PenerimaBantuanViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = PenerimaBantuan.objects.all()
    serializer_class = PenerimaBantuanSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        penerimabantuan = Warga.objects.filter(Status="disetujui")
        serializer = PenerimaBantuanSerializer(penerimabantuan, many=True)
        return Response({
            "status": True, "message": "Sukses !", "data_penerima_bantuan": serializer.data
        })
