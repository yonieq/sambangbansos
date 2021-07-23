import json
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def check_nik(nik=None):
    try:
        # return None
        endpoint = getattr(settings, "ENDPOINT", "")
        logger.debug(endpoint)
        if nik is not None:
            payload = {
                "nik": nik,
                "user_id": getattr(settings, "KAB_ID", "BANSOS"),
                "password": getattr(settings, "KAB_ID", "BrebesMaju"),
                "ip_user": getattr(settings, "KAB_ID", "10.29.33.10")
            }

            warga = None
            headers = {'Content-Type': 'application/json', 'User-Agent': 'SambangBansosV1'}
            api_request = requests.post(endpoint, headers=headers, data=json.dumps(payload))

            if api_request.status_code == 200:
                if "RESPON" not in api_request.text:
                    dictresponse = api_request.json()
                    # print(dictresponse)
                    logger.debug(dictresponse)
                    warga = dictresponse['content'][0]
            api_request.close()
            return warga
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None
