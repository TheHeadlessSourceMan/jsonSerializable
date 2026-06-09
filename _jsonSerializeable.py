#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Classes that can be serialized to json
"""
import typing
import collections
import json
try:
    import ezFs # type:ignore
    #TODO: feature temporarliy disabled due to library problems
    hasEzFs=False #True
except ImportError:
    hasEzFs=False
from paths import UrlCompatible,asURL

JsonPrimitive=typing.Union[str,int,float,bool]
JsonMember=typing.Union[JsonPrimitive,"JsonObj"]
JsonObj=typing.Union[typing.Iterable[JsonMember],typing.Dict[str,JsonMember]]
IsJsonObj=typing.Union[str,JsonObj] # can pass in str to convert


class JsonSerializeable:
    """
    Classes that can be serialized to json

    To implement this feature, one must
        1) inherit from this class
        2) implement a member called jsonObj
        3) (optional) set a DEFAULT_LOCATION

    will use EzFs if present, so you can get data from
    http, ftp, dropbox, or wherever
    """

    DEFAULT_LOCATION=None

    def __init__(self,
        location:typing.Optional[UrlCompatible]=None,
        jsonObj:typing.Optional[IsJsonObj]=None):
        """ """
        self._location:typing.Optional[UrlCompatible]=None
        self._jsonObj:typing.Optional[JsonObj]=None
        if location is not None:
            self.load(location)
        if jsonObj is not None:
            self.jsonObj=jsonObj

    def load(self,location:typing.Optional[UrlCompatible]=None)->None:
        """
        load a file
        """
        self.loadJson(location)
    def loadJson(self,location:typing.Optional[UrlCompatible]=None)->None:
        """
        Load from a json file
        """
        if location is None:
            if self._location is None:
                self._location=self.DEFAULT_LOCATION
            location=self._location
        else:
            self._location=location
        if location is None:
            return
        if hasEzFs:
            f=ezFs.EzFs().get(location)
        else:
            try:
                f=open(location,'rb')
            except FileNotFoundError:
                print('No file to load "%s"'%location)
        data=f.read()
        f.close()
        self.json=data

    def save(self,location:typing.Optional[UrlCompatible]=None)->None:
        """
        save a file
        """
        self.saveJson(location)
    def saveJson(self,location:typing.Optional[UrlCompatible]=None)->None:
        """
        Save the json file
        """
        if location is None:
            if self._location is None:
                self._location=self.DEFAULT_LOCATION
            location=self._location
        else:
            self._location=location
        data=self.json
        if hasEzFs:
            f=ezFs.EzFs().get(location)
        else:
            location=asURL(location)
            try:
                f=open(location,'wb')
            except FileNotFoundError:
                print('No file to write "%s"'%location)
        f.write(data.encode('utf-8'))
        f.close()

    @property
    def json(self)->str:
        """
        this object as a json string
        """
        return json.dumps(self.jsonObj)
    @json.setter
    def json(self,jsonString:str):
        self.jsonObj=json.loads(jsonString)


DictValueType=typing.TypeVar('DictValueType',bound=JsonSerializeable)
class JsonSerializableDict(
    typing.Generic[DictValueType],
    JsonSerializeable,
    collections.UserDict[str,DictValueType]):
    """
    A serializable dict of {name:DictValueType}

    The json can be either a dict, in which case the key is used as the name
    or a list, in which case the objects "name" member will be used as the key
    """
    def __init__(self,
        itemFactory:typing.Callable,
        location:typing.Optional[UrlCompatible]=None,
        jsonObj:typing.Optional[IsJsonObj]=None):
        """ """
        # NOTE: all object dict access is redirected to a self.data dict
        self.isDictNotArray=False
        self.itemFactory=itemFactory
        collections.UserDict.__init__(self)
        JsonSerializeable.__init__(self,location,jsonObj)

    @property # type: ignore
    def jsonObj(self
        )->typing.Union[
            typing.Dict[str,typing.Any],
            typing.List[typing.Dict[str,typing.Any]]]:
        """
        this as a saveable json object
        """
        if self.isDictNotArray:
            return {k:v.jsonObj for k,v in self.items()}
        return [v.jsonObj for v in self.values()]
    @jsonObj.setter
    def jsonObj(self,
        jsonObj:typing.Union[
            typing.Dict[str,typing.Any],
            typing.List[typing.Dict[str,typing.Any]]]):
        """
        this as a saveable json object
        """
        if isinstance(jsonObj,list):
            self.isDictNotArray=False
            self.data={}
            for j in jsonObj:
                newItem=self.itemFactory(jsonObj=j)
                self.data[newItem.name]=newItem
        else:
            self.isDictNotArray=True
            items=jsonObj.items()
            self.data={k:self.itemFactory(jsonObj=v) for k,v in items}


def cmdline(args):
    """
    Run the command line

    :param args: command line arguments (WITHOUT the location)
    """
    printhelp=False
    if not args:
        printhelp=True
    else:
        for arg in args:
            if arg.startswith('-'):
                arg=[a.strip() for a in arg.split('=',1)]
                if arg[0] in ['-h','--help']:
                    printhelp=True
                else:
                    print('ERR: unknown argument "'+arg[0]+'"')
            else:
                print('ERR: unknown argument "'+arg+'"')
    if printhelp:
        print('Usage:')
        print('  jsonSerializeable.py [options]')
        print('Options:')
        print('   NONE')
        return -1
    return 0


if __name__=='__main__':
    import sys
    sys.exit(cmdline(sys.argv[1:]))
