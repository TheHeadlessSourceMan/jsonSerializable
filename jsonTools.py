"""
Useful tools for working with JSON data
"""
import typing
from math import floor
from .types import JsonDict


def getJsonStr(
    d:JsonDict,
    name:str,
    default:typing.Union[None,str,typing.Type[IndexError]]=IndexError
    )->str:
    """
    Get json string from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=d.get(name,default)
    if ret==IndexError:
        raise IndexError(f'No Json value for {name}')
    if ret is None:
        return ret # type: ignore
    if not isinstance(ret,str):
        ret=str(ret)
    return ret

def getJsonFloat(
    d:JsonDict,
    name:str,
    default:typing.Union[None,float,typing.Type[IndexError]]=IndexError
    )->float:
    """
    Get json float from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=d.get(name,default)
    if ret==IndexError:
        raise IndexError(f'No Json value for {name}')
    if ret is None:
        return ret # type: ignore
    if not isinstance(ret,float):
        ret=float(ret) # type: ignore
    return ret

def getJsonInt(
    d:JsonDict,
    name:str,
    default:typing.Union[None,int,typing.Type[IndexError]]=IndexError
    )->int:
    """
    Get json int from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=d.get(name,default)
    if ret==IndexError:
        raise IndexError(f'No Json value for {name}')
    if ret is None:
        return ret # type: ignore
    if not isinstance(ret,int):
        ret=floor(float(ret)) # type: ignore
    return ret

def getJsonArray(
    d:JsonDict,
    name:str,
    default:typing.Union[None,typing.List,typing.Type[IndexError]]=IndexError
    )->typing.List:
    """
    Get untyped json array from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=d.get(name,default)
    if ret==IndexError:
        raise IndexError(f'No Json value for {name}')
    if ret is None:
        return ret # type: ignore
    if not isinstance(ret,list):
        ret=[ret]
    return ret

def getJsonStringArray(
    d:JsonDict,
    name:str,
    default:typing.Union[None,typing.List[str],typing.Type[IndexError]]=IndexError
    )->typing.List[str]:
    """
    Get string array from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=getJsonArray(d,name,default)
    if not isinstance(ret,list):
        return ret
    return [str(item) for item in ret]

def getJsonFloatArray(
    d:JsonDict,
    name:str,
    default:typing.Union[None,typing.List[float],typing.Type[IndexError]]=IndexError
    )->typing.List[float]:
    """
    Get float array from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=getJsonArray(d,name,default)
    if not isinstance(ret,list):
        return ret
    return [float(item) for item in ret]

def getJsonIntArray(
    d:JsonDict,
    name:str,
    default:typing.Union[None,typing.List[int],typing.Type[IndexError]]=IndexError
    )->typing.List[int]:
    """
    Get int array from a json object.
    Type cast if necessary.

    If default is not set, raises IndexError on missing value.
    """
    ret=getJsonArray(d,name,default)
    if not isinstance(ret,list):
        return ret
    return [floor(float(item)) for item in ret]
