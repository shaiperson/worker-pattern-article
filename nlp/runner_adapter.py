import logging
import language_detection

logger = logging.getLogger('Meme Classifier')


def run_language_detection(text: str):
    pred = language_detection.run(text)
    return {
        'language': pred.language,
        'probability': pred.probability,
    }
