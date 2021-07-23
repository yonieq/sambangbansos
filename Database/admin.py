from django.contrib import admin
from .models import Kecamatan, Desa, Rw, Rt, Keluarga, Warga, Bantuan, PenerimaBantuan, UserDesa


# Register your models here.

class DesaAdmin(admin.ModelAdmin):
    list_display = ('Kode', 'Nama', 'Kecamatan')


class KecamatanAdmin(admin.ModelAdmin):
    list_display = ('Kode', 'Nama')


class UserDesaAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Desa')


class PenerimaBantuanAdmin(admin.ModelAdmin):
    list_display = ('Bantuan', 'Keluarga')


class WargaAdmin(admin.ModelAdmin):
    list_display = ('Nik', 'Nama', 'Desa')
    search_fields = ['Nik', 'Nama']


class KeluargaAdmin(admin.ModelAdmin):
    list_display = ('NomerKK', 'Alamat', 'Rt', 'Rw', 'Desa')
    search_fields = ['NomerKK']





admin.site.register(Kecamatan, KecamatanAdmin)
admin.site.register(Desa, DesaAdmin)
admin.site.register(Rw)
admin.site.register(Rt)
admin.site.register(Keluarga, KeluargaAdmin)
admin.site.register(Warga, WargaAdmin)
admin.site.register(Bantuan)
admin.site.register(PenerimaBantuan, PenerimaBantuanAdmin)
admin.site.register(UserDesa, UserDesaAdmin)
