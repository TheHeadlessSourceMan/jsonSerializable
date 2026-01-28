"""
Json-related types
"""
import typing

JsonCompatible=typing.Union[str,bytes,
    typing.Dict[str,typing.Any],typing.IO,'HasJson','HasJsonFn']

JsonPrimitive=typing.Union[int,float,str]
JsonList=typing.Iterable['JsonLike']
JsonDict=typing.Dict[str,'JsonLike']
JsonObject=JsonDict
JsonLike=typing.Union[JsonPrimitive,JsonList,JsonDict]

class HasJson(typing.Protocol):
    """
    A class that has a .json member
    """
    json:JsonCompatible
class HasJsonFn(typing.Protocol):
    """
    A class that has a .json() member function
    """
    def json(self)->JsonCompatible:
        """
        return a json compatable object of some kind
        """
