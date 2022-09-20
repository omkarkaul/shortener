import secrets

from common.constants import Constants
from common.factory import Factory, Components


class Shortener:
    def __init__(self):
        self.dynamo_client = Factory.create(Components.DataClients.DynamoDB, table_name=Constants.SHORTENER_TABLE_NAME)

    def shorten(self, url):
        result = {}
        while not result:
            url_key = "".join(secrets.choice(Constants.KEY_ALPHABET) for _ in range(Constants.KEY_LENGTH))
            result = self._store_hash(url, url_key)
        return result

    def _store_hash(self, url, url_key):
        item = {
            "key": url_key,
            "url": url,
            "click": 0
        }
        return self.dynamo_client.insert_item(item)


