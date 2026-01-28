"""
The idea is that Text is a regular string that contains plain text
(as opposed to HTML or a URL or something else).

The reason it is needed is because sometimes we don't know whether
a function is returning java script code or just plain text.

Of course interesting features may attach to it over time.
"""
import typing

from paths import URL, URLCompatible, asURL, isUrlCompatible, LoadAndSave
from .baseTypes import TextCompatible, HtmlCompatible, _IHtmlTools_Html, _IHtmlTools_Text, isHtmlCompatible
from .conversions import html2txt, txt2html


class Text(_IHtmlTools_Text,LoadAndSave):
    """
    This class is a regular string that contains plain text.

    The reason it is needed is because sometimes we don't know whether
    a function is returning java script code or just plain text.
    
    Of course interesting features may attach to it over time.
    """
    
    DefaultFilename:str='UNDEFINED.txt'

    def __init__(self,text:TextCompatible=None,html:HtmlCompatible=None):
        LoadAndSave.__init__(self)
        self._text:str="" # always, always, always a string!
        self._url:typing.Union[URL,None]=None
        if text is not None:
            self.text=text
        elif html is not None:
            self.html=html

    def _encode(self):
        """
        encode this as bytes
        """
        return self._html.encode('utf-8')
    def _decode(self,data:bytes)->None:
        self.assignUnknownString(data)

    def assignUnknownString(self,s:typing.Union[str,bytes])->None:
        """
        If you don't know whether a string is html or plain text you can use this.

        If the first non-whitespace character is a "<", assigns as html, otherwise as plain text

        :param s: html or text
        :type s: str
        """
        from .html import Html
        self._filename=None
        if s is None:
            self._text=""
            return
        if isinstance(s,bytes):
            s=s.decode('utf-8','ignore') # TODO: is there a smarter way?
        if Html.looksLikeHtml(s) in (None,True):
            self.html=s
        else:
            self._text=s

    def load(self,url:typing.Union[URLCompatible,None]=None):
        """
        load a url
        
        NOTE: Use this when you don't know whether the file specified is plain text or html.
            If you do know, then use .html=URL(url) or .text=URL(url)
        """
        self.url=url

    def reload(self):
        """
        if there is a url specified, reload it
        """
        if self._url:
            self.html=self._url.read()

    @property
    def text(self)->str:
        return self._text
    @text.setter
    def text(self,text:TextCompatible):
        self._url=""
        if text is None:
            self._text=""
        elif isinstance(text,Text):
            self._url=text._url.copy()
            self._text=text._text
        elif isUrlCompatible(text,True):
            self._url=asURL(text)
            self._text=self._url.read()
        elif isHtmlCompatible(text,True):
            self.html=text 
        elif hasattr(text,'text'):
            text=text.text
            if callable(text):
                text=text()
            self.text=text # recursive, so the objects .text member can contain anything TextCompatible
        elif hasattr(text,'getText'):
            text=text.text
            if callable(text):
                text=text()
            self.text=text # recursive, so the objects .text member can contain anything TextCompatible
        elif isinstance(text,str):
            self._text=str
        elif isinstance(text,bytes):
            self._text=text.decode('utf-8','ignore')
        elif hasattr(text,'read') and callable(text.read):
            # sometimes, but not always, URL might have handled this instead
            text=text.read()
            if isinstance(text,bytes):
                text=text.decode('utf-8','ignore')
            self._text=text                
        else:
            # as a total catch-all case, if they pass in an arbitrary object, we stringify it and assign the results as best we can
            self.assignUnknownString(str(text))

    @property
    def html(self)->_IHtmlTools_Html:
        from .html import Html
        return Html(txt2html(self._text))
    @html.setter
    def html(self,html:typing.Union[HtmlCompatible,typing.Any]):
        self._url=None
        if hasattr(html,"text"):
            self._text=html.text
            return
        if isUrlCompatible(html,True):
            self._url=URL(html)
            html=self._url.read()
        elif hasattr(html,"read") and callable(html.read):
            html=html.read()
        if hasattr(html,"html"):
            if callable(html.read):
                html=html.html()
            else:
                html=html.html
        elif hasattr(html,"getHtml"):
            if callable(html.read):
                html=html.getHtml()
            else:
                html=html.getHtml
        if isinstance(html,bytes):
            html=html.decode('utf-8','ignore')
        if isinstance(html,str):
            self._text=html2txt(html)
        else:
            from .html import Html
            html=Html(html)
            self._text=html.text

    def assign(self,text:TextCompatible=None,html:HtmlCompatible=None):
        """
        Assign to html or plain text

        :param html: You can pass in URL objects, file-like objects, strings, etc!
        :type html: HtmlCompatible, optional
        :param text: You can pass in URL objects, file-like objects, strings, etc!
        :type text: PlaintextCompatible, optional
        """
        self._html:str="" # always, always, always a string!
        self._url:typing.Union[URL,None]=None
        if html is not None:
            self.html=html
        elif text is not None:
            self.text=text


    def __str__(self)->str:
        """
        this is the html string value, not plain text
        """
        return self._html


def asText(text:typing.Union[TextCompatible,typing.Any])->typing.Union[Text,None]:
    """
    Gets the text always as a Text object or None if it is None or "".
    If text is already a Text object, will not create a new one, otherwise, it always will.

    :param text: Can be:
        * another Text object
        * a properly-formatted Text string
        * any object with a (text,getText) data member
        * a readable file-like object
        * a paths.URL object
        * or Text or anything else will be converted with str() then that converted to Text
    :type text: hopefully TextCompatible, but can be anything
    :return: A Text object or None
    :rtype: Text|None
    """
    if text is None or (isinstance(text,(str,bytes)) and text==""):
        return None
    if isinstance(text,Text):
        return text
    return Text(text)