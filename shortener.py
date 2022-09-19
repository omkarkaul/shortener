from common.factory import Factory, Components


class Shortener:
    def __init__(self):
        dynamo_client = Factory.create(Components.DataClients.DynamoDB)

    def shorten(self, url):
        url_hash = self._get_hash(url)
        return self._store_hash(url_hash)

    def _get_hash(self, url):
        raise NotImplementedError()

    def _store_hash(self, url_hash):
        raise NotImplementedError()


