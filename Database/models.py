from django.db import models

# Create your models here.

BANTUAN_STATUS = [
    ('0', 'Usulan'),
    ('1', 'Disetujui'),
]

WARGA_STATUS = [
    ('usulan', 'Usulan'),
    ('disetujui', 'Disetujui'),
]


NON_AKTIF_STATUS = [
    ('0', 'Residu'),
    ('1', 'Double Data'),
    ('2', 'Belum Perekaman'),
    ('3', 'Meninggal'),
]


class Kecamatan(models.Model):
    Nama = models.CharField(max_length=100, unique=True, null=False)
    Kode = models.CharField(max_length=2, unique=True, null=False, db_index=True)

    def __str__(self):
        return self.Nama


class Desa(models.Model):
    Nama = models.CharField(max_length=100, unique=False, null=False)
    Kode = models.CharField(max_length=8, unique=True, null=False, db_index=True)
    Kecamatan = models.ForeignKey('Kecamatan', null=False, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.Nama


class Rw(models.Model):
    Nomer = models.IntegerField(null=False)

    def __str__(self):
        return self.Nomer


class Rt(models.Model):
    Nomer = models.IntegerField(null=False)

    def __str__(self):
        return self.Nomer


class Keluarga(models.Model):
    NomerKK = models.CharField(max_length=17, unique=True, null=False, db_index=True)
    Alamat = models.CharField(max_length=255, null=False)
    Rt = models.IntegerField(null=False, default=0)
    Rw = models.IntegerField(null=False, default=0)
    Desa = models.ForeignKey('Desa', unique=False, null=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('NomerKK',)

    def __str__(self):
        return self.NomerKK


class Warga(models.Model):
    Nik = models.CharField(max_length=17, unique=True, null=False, default='', db_index=True)
    Nama = models.CharField(max_length=100, null=False)
    TmpLahir = models.CharField(max_length=100, null=False)
    TglLahir = models.DateField(null=False)
    Alamat = models.CharField(max_length=255, null=False)
    Rt = models.IntegerField(null=False, default=0)
    Rw = models.IntegerField(null=False, default=0)
    NikValid = models.BooleanField(default=False, null=False, db_index=True)
    Desa = models.ForeignKey('Desa', unique=False, null=False, on_delete=models.CASCADE, db_index=True)
    Keluarga = models.ForeignKey('Keluarga', unique=False, null=False, default=None, on_delete=models.CASCADE)
    Status = models.CharField(
        max_length=10,
        choices=WARGA_STATUS,
        default='usulan',
        null=False
    )

    # class Meta:
    #   ordering = ('Nik', 'Desa')

    def __str__(self):
        return self.get_Status_display()


class NikChanged(models.Model):
    ReplacedNik = models.CharField(max_length=17, unique=True, null=False, default='')
    ReplacedDate = models.DateField(null=False)
    Warga = models.ForeignKey('Warga', unique=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.ReplacedNik


class Bantuan(models.Model):
    Nama = models.CharField(max_length=100, unique=True, null=False)
    Tahun = models.CharField(max_length=4, unique=False, null=False)
    Sumber = models.CharField(max_length=100, unique=False, null=False)

    def __str__(self):
        return self.Nama


class PenerimaBantuan(models.Model):
    Bantuan = models.ForeignKey('Bantuan', unique=False, null=False, on_delete=models.CASCADE, db_index=True)
    Keluarga = models.ForeignKey('Keluarga', unique=False, null=False, on_delete=models.CASCADE, db_index=True)
    Status = models.CharField(
        max_length=1,
        choices=BANTUAN_STATUS,
        default='0',
        null=False
    )
    TglPengajuan = models.DateField(default='2020-01-01', null=False)


class UserDesa(models.Model):
    Username = models.CharField(max_length=255, unique=True, null=False)
    Desa = models.ForeignKey('Desa', null=False, on_delete=models.CASCADE, db_index=True)


class StatusNonAktif(models.Model):
    Warga = models.ForeignKey('Warga', unique=False, null=False, on_delete=models.CASCADE)
    Status = models.CharField(
        max_length=1,
        choices=NON_AKTIF_STATUS,
        default='0',
        null=False
    )
    UpdateDate = models.DateField(default='2020-01-01', null=False)

