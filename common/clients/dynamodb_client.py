import boto3
from boto3.dynamodb.conditions import Key
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

    def exists(self, table):
        try:
            table.load()
            return True
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ResourceNotFoundException':
                return False
            raise Exception(f"Could not check for existence of table {self.table.name}")

    def create_table(self, table_name):
        try:
            self.table = self.client.create_table(
                TableName=table_name,
                KeySchema=Constants.SHORTENER_TABLE_KEY_SCHEMA,
                AttributeDefinitions=Constants.SHORTENER_TABLE_ATTRIBUTE_DEFS,
                ProvisionedThroughput=Constants.SHORTENER_THROUGHPUT
            )
            self.table.wait_until_exists()
            print(f'{table_name} table created!')
            return self.table
        except ClientError as ex:
            raise Exception(f'Could not create table "{table_name}":'
                            f' {ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')

    def insert_item(self, item):
        try:
            if not self.exists(self.table):
                self.create_table(self.table.name)

            insert_result = self.table.put_item(
                Item=item
            )
            if insert_result.get('ResponseMetadata').get('HTTPStatusCode') == Constants.HTTP_SUCCESS:
                print(f'Item insert succeeded {item}')
                return insert_result
            raise Exception(f'Failed to insert item {str(item)}')

        except ClientError as ex:
            raise Exception(f'Could not add item {str(item)} to table {self.table.name}: '
                            f'{ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')

    def delete_item(self, item):
        try:
            if not self.exists(self.table):
                raise Exception(f"{self.table.name} does not exist, cannot delete from table!")
            response = self.table.delete(Key=item)
            return response
        except ClientError as ex:
            raise Exception(f'Could not delete item {str(item)} from table {self.table.name}: '
                            f'{ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')

    def get_item(self, key, item):
        try:
            if not self.exists(self.table):
                raise Exception(f"{self.table.name} does not exist, cannot delete from table!")
            response = self.table.query(KeyConditionExpression=Key('key').eq(item))
            if response.get('ResponseMetadata').get('HTTPStatusCode') == Constants.HTTP_SUCCESS:
                return response.get('Items')
            raise Exception(f'Could not fetch item with key {key} from table {self.table.name}')
        except ClientError as ex:
            raise Exception(f'Could not list item {str(item)} with key {str(key)} from table {self.table.name}: '
                            f'{ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')

    def get_items(self):
        try:
            if not self.exists(self.table):
                raise Exception(f"{self.table.name} does not exist, cannot list items from table!")
            scan_response = self.table.scan()
            items = scan_response['Items']
            while 'LastEvaluatedKey' in scan_response:
                scan_response = self.table.scan(ExclusiveStartKey=scan_response['LastEvaluatedKey'])
                items.extend(scan_response['Items'])
            return items
        except ClientError as ex:
            raise Exception(f'Could not list items from table {self.table.name}: '
                            f'{ex.response["Error"]["Code"]}, {ex.response["Error"]["Message"]}')
