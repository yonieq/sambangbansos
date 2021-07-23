from django.db.models import fields
from rest_framework import serializers

from django.contrib.auth.models import User
from Database.models import Kecamatan, Desa, Bantuan, Keluarga, Warga, PenerimaBantuan


class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kecamatan
        fields = "__all__"


class DesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desa
        fields = "__all__"


class BantuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bantuan
        fields = "__all__"


class KeluargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keluarga
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'last_login', 'date_joined')


class WargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warga
        fields = "__all__"


class UsulanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warga
        fields = "__all__"


class PenerimaBantuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warga
        fields = "__all__"
