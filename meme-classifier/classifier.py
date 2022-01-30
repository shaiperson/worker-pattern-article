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


def pred_to_label(pred):
    i = np.argmax(pred)
    return labels[i]


def run_on_url(url):
    logger.debug('Fetching URL')
    response = requests.get(url)
    img_bytes = io.BytesIO(response.content)

    if not response.ok:
        raise exceptions.RequestError('', response)

    logger.debug('Reading and preparing image')
    img = tf.image.resize(PIL.Image.open(img_bytes), (150, 150))
    a = tf.keras.utils.img_to_array(img)
    t = tf.convert_to_tensor([a])

    logger.debug('Running on image')
    pred = model.predict(t)

    return pred_to_label(pred)
