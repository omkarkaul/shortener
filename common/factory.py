from enum import Enum

from common.clients.dynamodb_client import DynamoClient

class Components:
    class DataClients(Enum):
        DynamoDB = 1

class Factory:
    @staticmethod
    def create(component_type, **kwargs):
        if isinstance(component_type, Components.DataClients):
            return Factory._create_data_client(component_type, **kwargs)
        return None

    @staticmethod
    def _create_data_client(component_type, **kwargs):
        if component_type == Components.DataClients.DynamoDB:
            return DynamoClient(table_name=kwargs.get('table_name'))
        return None
