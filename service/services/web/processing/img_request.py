import base64

import cv2
import numpy as np
import requests


class URLError(Exception):
    pass


class Base64Error(Exception):
    pass


def bytes2img(data):
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)


def load_image(url=None, b64str=None):
    if url:
        try:
            r = requests.get(url, verify=False)
            if r.status_code == 200:
                return bytes2img(r.content)
        except Exception as err:
            raise URLError(err)
    if b64str:
        try:
            return bytes2img(base64.b64decode(b64str))
        except Exception as err:
            raise Base64Error(err)
