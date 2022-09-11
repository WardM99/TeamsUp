"""utils for the schemas"""
# pylint: disable=too-few-public-methods
from humps import camelize # type: ignore
from pydantic import BaseModel


def to_camel(string: str) -> str:
    """Return the camel case version of a given string"""
    return camelize(string)


class CamelCaseModel(BaseModel):
    """Base model that converts snake to camel case when serialized"""

    class Config:
        """Config"""
        alias_generator = to_camel
        allow_population_by_field_name = True


class OrmModel(CamelCaseModel):
    """Orm model"""

    class Config:
        """Set to ARM mode"""
        orm_mode = True
