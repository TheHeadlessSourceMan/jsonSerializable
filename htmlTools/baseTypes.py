import typing
from paths import URLCompatible,isUrlCompatible


class _IHtmlTools_Html:
    """
    A Base class mainly intented to solve both unique identity and circular import issues
    """

class _IHtmlTools_Text:
    """
    A Base class mainly intented to solve both unique identity and circular import issues
    """


class HasRead(typing.Protocol):
    """
    Duck typing for any object that has a .read() member
        (AKA, file-like objects)
    """
    def read(self,*args) -> typing.Union[str,bytes]:
       ...  # Empty method body (explicit '...')


class HasHtml(typing.Protocol):
    """
    Duck typing for any object that has a .html member
    """
    html:"HtmlCompatible"

    
class HasText(typing.Protocol):
    """
    Duck typing for any object that has a .text member
    """
    text:"PlaintextCompatible"


PlaintextCompatibleStrict=typing.Union[_IHtmlTools_Text,HasText]
PlaintextCompatible=typing.Union[URLCompatible,PlaintextCompatibleStrict,str,bytes,HasHtml,HasRead]
TextCompatibleStrict=PlaintextCompatibleStrict
TextCompatible=PlaintextCompatible

HtmlCompatibleStrict=typing.Union[_IHtmlTools_Html,HasHtml]
HtmlCompatible=typing.Union[URLCompatible,HtmlCompatibleStrict,str,bytes,HasText,HasRead]


def isReadable(obj:typing.Any)->bool:
    return hasattr(obj,'read') and callable(obj.read)


def isPlaintextCompatible(obj:typing.Any,strict=False)->bool:
    """
    Determine if a variable is plaintext compatible

    :param obj: anything
    :type obj: typing.Any
    :param strict: whether to disallow generic things like str, defaults to False
    :type strict: bool, optional
    :return: wheter obj is compatible with creating a plain Text() object
    :rtype: bool
    """
    if not strict:
        if isinstance(obj,(str,bytes)) or hasattr(obj,'html') or hasattr(obj,'getHtml') or isReadable(obj) or isUrlCompatible(obj):
            return True
    return isinstance(obj,_IHtmlTools_Text) or hasattr(obj,'text') or hasattr(obj,'getText')



def isHtmlCompatible(obj:typing.Any,strict=False)->bool:
    """
    Determine if a variable is html compatible

    :param obj: anything
    :type obj: typing.Any
    :param strict: whether to disallow generic things like str, defaults to False
    :type strict: bool, optional
    :return: wheter obj is compatible with creating an Html() object
    :rtype: bool
    """
    if not strict:
        if isinstance(obj,(str,bytes)) or hasattr(obj,'text')  or hasattr(obj,'getText') or isReadable(obj) or isUrlCompatible(obj):
            return True
    return isinstance(obj,_IHtmlTools_Html) or hasattr(obj,'html')  or hasattr(obj,'getHtml')