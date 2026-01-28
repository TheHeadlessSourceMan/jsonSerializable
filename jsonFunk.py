"""
A down-and-dirty object that wraps JSON data
"""
import typing
from collections.abc import Mapping
import json
from .types import JsonCompatible


class JsonFunk:
    """
    A down-and-dirty object that wraps JSON data

    TODO: should probably merge into JsonMapped, etc
    """

    def __init__(self,filename:typing.Optional[str],
        jsonData:typing.Optional[JsonCompatible]=None):
        """
        """
        self._jsonObj:typing.Dict[str,typing.Any]={}
        if jsonData is not None:
            self.json=jsonData # type: ignore
        if filename is not None:
            self.load(filename)

    def __getattr__(self, __name: str) -> typing.Any:
        return self.jsonObj[__name]

    @property
    def json(self)->str:
        """
        This object as a json string
        """
        return json.dumps(self.jsonObj)
    @json.setter
    def json(self,jsonObj:JsonCompatible):
        """
        Can assign to a string, raw bytes,
            a json dict, a file-like object,
            or an object with a json member value or function
        """
        if isinstance(jsonObj,str):
            self.jsonObj=json.loads(jsonObj)
        elif isinstance(jsonObj,bytes):
            self.jsonObj=json.loads(jsonObj.decode('UTF-8',errors='ignore'))
        elif hasattr(jsonObj,'json'):
            jsonAttr=getattr(jsonObj,'json')
            if callable(jsonAttr):
                jsonAttr=jsonAttr()
            self.json=jsonAttr
        elif hasattr(jsonObj,'read'):
            self.json=jsonObj.read()
        elif isinstance(jsonObj,Mapping):
            self.jsonObj=jsonObj
        else:
            msg=f'Incompatible JSON type: {jsonObj.__class__.__name__}'
            raise Exception(msg)
    @property
    def jsonObj(self)->typing.Dict[str,typing.Any]:
        """
        This object as a JSON-compatible object
        """
        return self._jsonObj
    @jsonObj.setter
    def jsonObj(self,jsonObj:JsonCompatible):
        if isinstance(jsonObj,Mapping):
            self.clear()
            self._jsonObj=jsonObj
        else:
            self.json=jsonObj # type:ignore

    def limitedJsonObj(self,
        keys:typing.Union[typing.Callable,typing.Dict,typing.Iterable[str]]
        )->typing.Dict[str,typing.Any]:
        """
        get jsonObj, but limited to a set of keys

        :keys: a list of keys, dict to steal keys from,
            or function whose parameters to use as keys
        """
        if isinstance(keys,Mapping):
            keys=keys.keys()
        if callable(keys):
            keys=keys.__code__.co_varnames # type: ignore
            if keys and keys[0] in ('self','cls'):
                if len(keys)>1:
                    keys=keys[1:]
                else:
                    return {}
        ret:typing.Dict[str,typing.Any]={}
        for key in typing.cast(typing.List[str],keys):
            if key in self._jsonObj:
                ret[key]=self._jsonObj[key]
        return ret

    def clear(self)->None:
        """
        To be overriden by children to clear cached data when json changes
        """

    def load(self,configFilename:str)->None:
        """
        Load settings from a json file
        """
        with open(configFilename,'rb') as f:
            self.json=f # type:ignore

    def save(self,configFilename:str)->None:
        """
        Save settings to a json file
        """
        with open(configFilename,'wb') as f:
            f.write(self.json.encode('UTF-8',errors="ignore"))

    def __repr__(self):
        return self.json
