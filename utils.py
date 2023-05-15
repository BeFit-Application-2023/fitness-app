import io
import cv2
import base64

import numpy as np
from PIL import Image


def frame_decode(base64_string):
    idx = base64_string.find('base64,')
    base64_string  = base64_string[idx+7:]

    sbuf = io.BytesIO()

    sbuf.write(base64.b64decode(base64_string, ' /'))
    pimg = Image.open(sbuf)

    return np.array(pimg)


def frame_encode(frame):
    img_encode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]

    # base64 encode
    string_data = base64.b64encode(img_encode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    string_data = b64_src + string_data
    return string_data


def moving_average(x):
    return np.mean(x)


def body_mass_index(height, weight):
    return round(height / (weight / 100) ** 2, 2)