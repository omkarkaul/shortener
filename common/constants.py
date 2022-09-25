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