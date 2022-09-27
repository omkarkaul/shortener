class Constants:
    LOCAL = 'local'
    PROD = 'prod'
    KEY_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    KEY_LENGTH = 5
    LOCAL_DYNAMO_URL = "http://localhost:8000"
    SHORTENER_TABLE_NAME = "shortener"
    SHORTENER_TABLE_KEY_SCHEMA = [
        {'AttributeName': 'key', 'KeyType': 'HASH'},
    ]
    SHORTENER_TABLE_ATTRIBUTE_DEFS = [
        {'AttributeName': 'key', 'AttributeType': 'S'},
    ]
    SHORTENER_THROUGHPUT = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
    HTTP_SUCCESS = 200
    HTTP_SUCCESS_MESSAGE = "Success"
    HTTP_CREATED = 201
    HTTP_CREATED_MESSAGE = 'Created'
    HTTP_SERVER_FAIL = 500
    HTTP_SERVER_FAIL_MESSAGE = "Server error"
    HTTP_BAD_REQUEST = 400
    HTTP_BAD_REQUEST_MESSAGE = "Bad request"
    HTTP_NOT_FOUND = 404
    HTTP_NOT_FOUND_MESSAGE = "Not found"
