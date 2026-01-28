"""
Extends JsonFunk for a weird, experimental InfoClass pattern.

This pattern works like:
    1) info about how an object works is loaded from file
        (into an InfoClass object)
    2) that object is treated like a class and used to create the
        actual object

Example:
    NewClass=InfoClass(createsClass=OriginalClass,"info.json")
    obj=NewClass(originalClassParams)
    isinstance(NewClass,OriginalClass) == True
    print(obj.info.my_json_param)
"""
import typing
from .jsonFunk import JsonFunk
from .types import JsonCompatible


class InfoClass(JsonFunk):
    """
    Extends JsonFunk for a weird, experimental InfoClass pattern.

    This pattern works like:
        1) info about how an object works is loaded from file
            (into an InfoClass object)
        2) that object is treated like a class and used to create the
            actual object

    Example:
        NewClass=InfoClass(createsClass=OriginalClass,"info.json")
        obj=NewClass(originalClassParams)
        isinstance(NewClass,OriginalClass) == True
        print(obj.info.my_json_param)
    """
    def __init__(self,createsClass:typing.Any,
        filename:typing.Optional[str],
        jsonData:typing.Optional[JsonCompatible]=None):
        """ """
        JsonFunk.__init__(self,filename,jsonData)
        self.createsClass=createsClass

    def __call__(self,**params)->typing.Any:
        """
        Create a new class

        Basically makes InfoClass act like a class,
        and this acts as the constructor by spitting
        out an object!
        """
        return self.create(**params)

    def create(self,**params)->typing.Any:
        """
        Create a new class
        """
        obj=self.createsClass(params)
        obj.info=self
        return obj
