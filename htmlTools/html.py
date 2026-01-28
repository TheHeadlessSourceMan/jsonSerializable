"""
The idea is that Html is a regular string that contains Html.

The reason it is needed is because sometimes we don't know whether
a function is returning java script code or just plain text.

Of course interesting features may attach to it over time.
"""
import typing
from paths import URL, URLCompatible, asURL, isUrlCompatible, LoadAndSave
from .baseTypes import HtmlCompatible, PlaintextCompatible, _IHtmlTools_Html, isPlaintextCompatible
from .conversions import html2txt, txt2html


class Html(_IHtmlTools_Html,LoadAndSave):
    """
    This class is a regular string that contains Html.

    The reason it is needed is because sometimes we don't know whether
    a function is returning java script code or just plain text.
    
    Of course interesting features may attach to it over time.
    
    TODO: integrate with http://w3lib.readthedocs.org
    """

    DefaultFilename:str='UNDEFINED.html'

    def __init__(self,html:HtmlCompatible=None,text:PlaintextCompatible=None):
        LoadAndSave.__init__(self)
        self._html:str="" # always, always, always a string!
        self._lxmlEtree=None
        if html is not None:
            self.html=html
        elif text is not None:
            self.text=text

    @property
    def dom(self):
        """
        get/set the current html as a dom (minidom) tree

        NOTE: can throw an error if not strictly-valid xml
        """
        import xml.dom.minidom
        return xml.dom.minidom.parseString(self.html)
    @dom.setter
    def dom(self,dom):
        """
        get/set the current html as a dom (minidom) tree
        """
        self.html=dom.toprettyxml()

    def makePrettyXML(self)->None:
        """
        Supposing this is xml compatible, format it pretty-like
        """
        self.dom=self.dom

    def makePretty(self)->None:
        """
        Attempt to reformat the document pretty-like
        """
        try:
            self.makePrettyXML()
        except Exception:
            pass

    @property
    def lxml(self)->typing.Any:
        """
        get current html as an lxml etree object
        """
        return self.etree
    @lxml.setter
    def lxml(self,lxml):
        """
        get current html as an lxml etree object
        """
        self.etree=lxml
    @property
    def etree(self)->typing.Any:
        """
        get current html as an lxml etree object
        """
        if self._lxmlEtree is None:
            try:
                #import lxml.etree
                from lxml.html.soupparser import fromstring
            except ImportError as e:
                print("ERR: Unable to find lxml. Install with:")
                print("   pip install lxml")
                print()
                raise(e)
            #parser=lxml.etree.HTMLParser()
            #lxml.etree.parse(StringIO(broken_html), parser)
            self._lxmlEtree=fromstring(self._html)
    @etree.setter
    def etree(self,etree):
        """
        get current html as an lxml etree object
        """
        self._lxmlEtree=etree
        self._html=etree.tostring()

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
        self._filename=None
        if s is None:
            self._html=""
            return
        if isinstance(s,bytes):
            s=s.decode('utf-8','ignore') # TODO: is there a smarter way?
        if Html.looksLikeHtml(s) in (None,True):
            self._html=s
        else:
            self.text=s

    @classmethod
    def looksLikeHtml(s:str):
        """
        Determine if the string looks like html.

        If the first non-whitespace character is a "<", assigns as html, otherwise as plain text

        If the string is blank, returns None

        :param s: [description]
        :type s: str
        """
        if s is None:
            return None
        for c in s:
            if c=='<':
                return True
            if c not in (' ','\t','\r','\n'):
                return False
        return None

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
        from .text import Text
        return Text(html2txt(self._html))
    @text.setter
    def text(self,text:typing.Union[PlaintextCompatible,typing.Any]):
        self._url=None
        if hasattr(text,"html"):
            self._html=text.html
            return
        if isUrlCompatible(text,True):
            self._url=URL(text)
            text=self._url.read()
        elif hasattr(text,"read") and callable(text.read):
            text=text.read()
        if hasattr(text,"text"):
            text=text.text
        if isinstance(text,bytes):
            text=text.decode('utf-8','ignore')
        if isinstance(text,str):
            self._html=txt2html(text)
        else:
            from .text import Text
            text=Text(text)
            self._html=text.html

    @property
    def html(self)->str:
        return self._html
    @html.setter
    def html(self,html:typing.Union[HtmlCompatible,typing.Any]):
        self._url=""
        if html is None:
            self._html=""
        elif isinstance(html,Html):
            self._url=html._url.copy()
            self._html=html._html
        elif isUrlCompatible(html,True):
            self._url=asURL(html)
            self._html=self._url.read()
        elif isPlaintextCompatible(html,True):
            self.text=html 
        elif hasattr(html,'html'):
            html=html.html
            if callable(html):
                html=html()
            self.html=html # recursive, so the objects .html member can contain anything HtmlCompatible
        elif isinstance(html,str):
            self._html=str
        elif isinstance(html,bytes):
            self._html=html.decode('utf-8','ignore')
        elif hasattr(html,'read') and callable(html.read):
            # sometimes, but not always, URL might have handled this instead
            html=html.read()
            if isinstance(html,bytes):
                html=html.decode('utf-8','ignore')
            self._html=html                
        else:
            # as a total catch-all case, if they pass in an arbitrary object, we stringify it and assign the results as best we can
            self.assignUnknownString(str(html))

    def assign(self,html:HtmlCompatible=None,text:PlaintextCompatible=None):
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


def asHtml(html:typing.Union[HtmlCompatible,typing.Any])->typing.Union[Html,None]:
    """
    Gets the html always as a Html object or None if it is None or "".
    If html is already a Html object, will not create a new one, otherwise, it always will.

    :param html: Can be:
        * another Html object
        * a properly-formatted Html string
        * any object with a (html,getHtml) data member
        * a readable file-like object
        * a paths.URL object
        * or Text or anything else will be converted with str() then that converted to html
    :type html: hopefully HtmlCompatible, but can be anything
    :return: A Html object or None
    :rtype: Html|None
    """
    if html is None or (isinstance(html,(str,bytes)) and html==""):
        return None
    if isinstance(html,Html):
        return html
    return Html(html)