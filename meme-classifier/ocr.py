from PIL import Image
import logging

import numpy as np
import cv2
import pytesseract

import imgutils

logger = logging.getLogger('Classifier')


def preprocess_final(im):
    im = cv2.bilateralFilter(im,5, 55,60)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, im = cv2.threshold(im, 240, 255, 1)
    return im


def run_on_url(url):
    logger.debug('Fetching image')
    img_bytes = imgutils.image_url_to_bytes(url)

    img_np = np.array(Image.open(img_bytes))
    img_preprocessed = preprocess_final(img_np)

    custom_config = r"--oem 3 --psm 11 -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '"
    text = pytesseract.image_to_string(img_preprocessed, lang='eng', config=custom_config)

    return text.replace('\n', '')
