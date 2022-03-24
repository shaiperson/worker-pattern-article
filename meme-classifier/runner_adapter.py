import classifier
import logging

logger = logging.getLogger('Adapter')


def run_meme_classifier(image_url):
    # logger.info('Running classifier on URL'.format(image_url))
    label, score = classifier.run_on_url(image_url)
    return {'label': label, 'score': float(f'{score:.5f}')}
