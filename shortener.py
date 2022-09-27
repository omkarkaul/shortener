import secrets

from common.constants import Constants
from common.factory import Factory, Components
from helpers.shortener_helpers import handle_exception, build_response


class Shortener:
    def __init__(self):
        self.dynamo_client = Factory.create(Components.DataClients.DynamoDB, table_name=Constants.SHORTENER_TABLE_NAME)

    @handle_exception
    def get_url(self, key_name):
        raise Exception('this is a test exception')
        response = self.dynamo_client.get_item(key='key', item=key_name)
        return build_response(
            status=Constants.HTTP_SUCCESS,
            message=Constants.HTTP_SUCCESS_MESSAGE,
            result={"url": response[0].get('url')}
        )

    @handle_exception
    def store_url(self, url):
        result = {}
        while not result:
            url_key = "".join(secrets.choice(Constants.KEY_ALPHABET) for _ in range(Constants.KEY_LENGTH))
            result = self._store_hash(url, url_key)
        return build_response(
            status=Constants.HTTP_SUCCESS,
            message=Constants.HTTP_SUCCESS_MESSAGE,
            result=result
        )

    def _store_hash(self, url, url_key):
        item = {
            "key": url_key,
            "url": url,
            "clicks": 0
        }
        return self.dynamo_client.insert_item(item)


