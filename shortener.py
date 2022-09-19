import secrets

from common.constants import Constants
from common.factory import Factory, Components


class Shortener:
    def __init__(self):
        dynamo_client = Factory.create(Components.DataClients.DynamoDB)

    def shorten(self, url):
        url_key = "".join(secrets.choice(Constants.KEY_ALPHABET) for _ in range(Constants.KEY_LENGTH))
        return self._store_hash(url, url_key)

    def _store_hash(self, url, url_key):
        raise NotImplementedError()


