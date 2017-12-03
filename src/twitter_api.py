from twython import Twython
import logging

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_settings(file):
    """
    Get api and access-token keys from the settings file
    :param file: name of the file containing api and access-token keys in order
                 "api_key", "api_secret", "access_token_key", "access_token_secret"
    :return: {api_key_name: api_key_value}
    """
    with open(file, "r") as settings:
        values = [line.strip() for line in settings]
    return dict(zip(["api_key", "api_secret", "access_token_key", "access_token_secret"], values))


params = get_settings('../settings.txt')
logging.info('Twitter API and access-token keys: {}'.format(params))
