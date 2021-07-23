import logging

from Database.models import Keluarga
from .desa import get_desa

logger = logging.getLogger(__name__)


def get_keluarga(nomerkk, jsondata):
    desa = str(jsondata['NO_KEC']).zfill(2) + '.' + str(jsondata['NO_KEL']) + '.'
    kk = Keluarga.objects.filter(NomerKK=nomerkk)
    if kk.count() <= 0:
        keluarga = Keluarga(NomerKK=jsondata["NO_KK"], Alamat=jsondata["ALAMAT"], Rt=jsondata["NO_RT"],
                            Rw=jsondata["NO_RW"], Desa=get_desa(desa))
        keluarga.save()
        return keluarga

    obj_kk = kk.first()
    return update_keluarga(obj_kk, jsondata)
    # return obj_kk


def update_keluarga(keluarga, jsondata):
    try:
        desa = str(jsondata['NO_KEC']).zfill(2) + '.' + str(jsondata['NO_KEL']) + '.'
        keluarga.NomerKK = jsondata["NO_KK"]
        keluarga.Alamat = jsondata["ALAMAT"]
        keluarga.Rt = jsondata["NO_RT"]
        keluarga.Rw = jsondata["NO_RW"]
        keluarga.Desa = get_desa(desa)
        keluarga.save()
        return keluarga
    except Exception as e:
        logger.error(e)
        return keluarga
