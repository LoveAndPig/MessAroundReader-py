from enum import Enum, unique


@unique
class ResourceType(Enum):
    TEXT = 1,
    IMAGE = 2,
    LINK = 3,
    INVALID = 4,


class Resource:
    def __init__(self, resource_type: ResourceType, resource_data: str):
        self.__type = resource_type
        self.__data = resource_data

    def get_type(self) -> ResourceType:
        return self.__type

    def get_data(self) -> str:
        return self.__data
