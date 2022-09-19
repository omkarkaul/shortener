from enum import Enum

from common.settings import Settings
from common.constants import Constants

class Components:
    class DataClients(Enum):
        DynamoDB = 1

class Factory:
    @staticmethod
    def create(component_type, **kwargs):
        if isinstance(component_type, Components.DataClients.DynamoDB):
            return Factory._create_data_client(component_type, **kwargs)
        return None

    @staticmethod
    def _create_data_client(component_type, **kwargs):
        if component_type == Components.DataClients.DynamoDB:
            if Settings.ENV == Constants.LOCAL:
                return None
            elif Settings.ENV == Constants.PROD:
                return None
        return None