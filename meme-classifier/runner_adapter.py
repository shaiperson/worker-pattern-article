import classifier
import adder
import logging

logger = logging.getLogger('Adapter')


def run_meme_classifier(image_url: str):
    # logger.info('Running classifier on URL'.format(image_url))
    label, score = classifier.run_on_url(image_url)
    return {'label': label, 'score': float(f'{score:.5f}')}


def run_add_numbers(x1: float, x2: float):
    return adder.run(x1, x2)
