"""
experimental class to map class member values to/from JSON objects

it features overrideable laod() and save()
so that it works with other similar objects
eg
    myObj.loadJson("filename.json")
    myObj.loadXml("filename.xml")
    myObj.load("to be determined by class")
"""
import typing
import json
from paths import LoadAndSave,URLCompatible
from .types import JsonDict


class JsonMapped(LoadAndSave):
    """
    experimental class to map class member values to/from JSON objects

    it features overrideable laod() and save()
    so that it works with other similar objects
    eg
        myObj.loadJson("filename.json")
        myObj.loadXml("filename.xml")
        myObj.load("to be determined by class")
    """

    # Used to map json to this object
    JSON_TABLE={} # {"jsonName":"memberName"}
    JSON_CLASSES={} # map json variable names to classes {"memberName":"className"} # noqa: E501 # pylint: disable=line-too-long

    def __init__(self,
        filename:typing.Optional[URLCompatible]=None,
        jsonData:typing.Union[None,str,typing.Dict]=None):
        """
        :param filename: try to load this file upon startup, defaults to None
        :type filename: typing.Optional[URLCompatible], optional
        :param jsonData: try to decode this json string/dict on startup
            defaults to None
        :type jsonData: typing.Union[None,str,typing.Dict], optional
        """
        LoadAndSave.__init__(self)
        self._JSON_load_and_save:LoadAndSave=LoadAndSave()
        self._JSON_load_and_save.defaultFilename=\
            self.__class__.__name__+'.json'
        self._JSON_load_and_save.decodeJson=self._decodeJson
        self._JSON_load_and_save.encode=self._encodeJson
        if filename is not None:
            self.loadJson(filename)
        if jsonData is not None:
            self.json=jsonData

    @property
    def DEFAULT_FILENAME(self):
        """
        Get the default filename for this type
        """
        return self.__class__.__name__+'.json'

    def _encodeJson(self)->str:
        """
        Encode this object as a JSON string
        """
        return self.jsonString
    _encode=_encodeJson # type: ignore

    def _decodeJson(self,data:str)->None:
        """
        Decode this object from a JSON string
        """
        self.jsonString=data
    _decode=_decodeJson # type: ignore

    @property
    def json(self)->str:
        """
        a JSON string, but can be assigned anything json-ish
            (open file, json string, json object, etc)
        generally it is better policy to be more specific with self.jsonString
        or self.jsonObject
        """
        return self.jsonString
    @json.setter
    def json(self,json:typing.Union[str,bytes,typing.IO,JsonDict]):
        if isinstance(json,(str,bytes,typing.IO)):
            self.jsonString=json
        else:
            self.jsonObject=json # type: ignore
    @property
    def jsonString(self)->str:
        """
        this object represented as a json string
        """
        return json.dumps(self.jsonObject)
    @jsonString.setter
    def jsonString(self,jsonString:typing.Union[str,bytes,typing.IO]):
        if isinstance(jsonString,typing.IO):
            jsonString=jsonString.read()
        self.jsonObject=json.loads(jsonString) # type: ignore
    @property
    def jsonObject(self)->JsonDict:
        """
        Get just the data from this object in a way that
        can be represented as json

        :return: [description]
        """
        if hasattr(super,"jsonObject"):
            thisObj=super.jsonObject # type: ignore
        else:
            thisObj={}
        for localName,jsonName in self.JSON_TABLE.items():
            if hasattr(self,localName):
                val=getattr(self,localName)
                if val is not None \
                    and not (
                        isinstance(val,(str,list,tuple,dict)) \
                        or val
                    ):
                    thisObj[jsonName]=val
        return thisObj
    @jsonObject.setter
    def jsonObject(self,jsonObject:JsonDict):
        if hasattr(super,'jsonObject'):
            super.jsonObject=jsonObject # type: ignore
        for k,v in jsonObject.items():
            localName=self.JSON_TABLE.get(k)
            if localName is not None:
                classConvert=self.JSON_CLASSES.get(k)
                if classConvert is not None:
                    v=classConvert()
                    v.jsonObject=v
                setattr(self,localName,v)

    def loadJson(self,
        filename:typing.Optional[URLCompatible]=None,
        altDecoder:typing.Optional[typing.Callable[[str],str]]=None,
        altDecoderParams:typing.Optional[typing.Dict]=None
        )->None:
        """
        load this object from json file/filename

        alias for loadJson(), which is usually preferred as
        some derived class may override load()
        """
        self._JSON_load_and_save.load(filename,altDecoder,altDecoderParams)
    load=loadJson

    def saveJson(self,
        filename:typing.Optional[URLCompatible]=None,
        altEncoder:typing.Optional[typing.Callable[...,str]]=None,
        altEncoderParams: typing.Optional[typing.Dict]=None
        )->None:
        """
        save this object to json file/filename

        alias for saveJson(), which is usually preferred as
        some derived class may override save()
        """
        self._JSON_load_and_save.save(filename,altEncoder,altEncoderParams)
    save=saveJson

    def __repr__(self)->str:
        return self.jsonString
