import requests
import PIL
import io
import logging

import numpy as np
import tensorflow as tf

from labels import labels
import exceptions

logger = logging.getLogger('Classifier')

# Load and compile model
logger.info('Loading model')
with open('model/meme-classifier-model.json') as f:
    model = tf.keras.models.model_from_json(f.read())

logger.info('Compiling model')
model.load_weights('model/meme-classifier-model.h5')
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy'],
)


def _pred_to_label(pred):
    i = np.argmax(pred)
    return labels[i]


def _get_image_bytes(url):
    response = requests.get(url)
    if not response.ok:
        raise exceptions.RequestError('', response)
    return io.BytesIO(response.content)


def _get_image_tensor(image_bytes):
    img = tf.image.resize(PIL.Image.open(image_bytes), (150, 150))
    a = tf.keras.utils.img_to_array(img)
    return tf.convert_to_tensor([a])


def run_on_url(url):
    logger.debug('Fetching image')
    image_bytes = _get_image_bytes(url)

    logger.debug('Reading and preparing image')
    image_tensor = _get_image_tensor(image_bytes)

    logger.debug('Running on image')
    pred = model.predict(image_tensor)

    res_i = pred.argmax()

    # return (label, score)
    return labels[res_i], pred.take(res_i)
