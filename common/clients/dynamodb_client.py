import boto3
from botocore.exceptions import ClientError

from common.constants import Constants
from common.settings import Settings


def _get_dynamo_client():
    if Settings.ENV == Constants.LOCAL:
        return boto3.resource(
            'dynamodb',
            region_name=Constants.LOCAL,
            endpoint_url=Constants.LOCAL_DYNAMO_URL
        )
    elif Settings.ENV == Constants.PROD:
        return boto3.resource('dynamodb')

    raise Exception(f'Current environment "{Settings.ENV}" is invalid, cannot generate Dynamo client!')


class DynamoClient:
    def __init__(self, table_name):
        self.client = _get_dynamo_client()
        self.table = self.client.Table(table_name)

    def exists(self, table_name):
        try:
            table = self.client.Table(table_name)
            table.load()
            return True
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ResourceNotFoundException':
                return False
            raise Exception(f"Could not check for existence of table {table_name}")

    def create_table(self, table_name):
        try:
            self.table = self.client.create_table(
                TableName=table_name,
                KeySchema=Constants.SHORTENER_TABLE_KEY_SCHEMA,
                AttributeDefinitions=Constants.SHORTENER_TABLE_ATTRIBUTE_DEFS
            )
            self.table.wait_until_exists()
            return self.table
        except ClientError as ex:
            raise Exception(f'Could not create table "{table_name}": {ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')

    def insert_item(self, item):
        try:
            if self.table:
                return self.table.put_item(
                    Item=item
                )
            raise Exception("Table not set")
        except ClientError as ex:
            raise Exception(f'Could not add item {str(item)} to table {self.table.name}: {ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')
