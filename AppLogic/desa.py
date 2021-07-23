from Database.models import Desa


def get_desa(kodedesa):
    desa = Desa.objects.filter(Kode=kodedesa)
    if desa.count() > 0:
        return desa[0]
    return None
