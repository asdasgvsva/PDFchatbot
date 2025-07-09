import random

def find_best_image(headline, images):
    """
    headline: str
    images: list of dicts, each with 'url', 'tags', 'description'
    """
    if not images:
        return None
    return random.choice(images)['url']
