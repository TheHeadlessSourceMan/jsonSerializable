"""
Base class for classes that want to have both html and text.

Derived classes MUST implement either Html or Text.  This way one can always
convert to the other.  If one of these is not implemented, then a circular
loop will occour.

NOTE: You probably don't ever want to say isinstance(x,HtmlAndText).
    It is much more versitile to use the isHtmlCompatible(x) and/or
    isPlaintextCompatible(x) functions
"""
import htmlTools


class HtmlAndText:
    """
    Base class for classes that want to have both html and text.

    Derived classes MUST implement either Html or Text.  This way one can always
    convert to the other.  If one of these is not implemented, then a circular
    loop will occour.

    NOTE: You probably don't ever want to say isinstance(x,HtmlAndText).
        It is much more versitile to use the isHtmlCompatible(x) and/or
        isPlaintextCompatible(x) functions
    """

    @property
    def html(self)->htmlTools.HtmlCompatibleStrict:
        """
        the self.text value auto-converted to html
        """
        return self.text.html
    @html.setter
    def html(self,html:htmlTools.HtmlCompatible):
        return htmlTools.asHtml(html)

    @property
    def text(self)->htmlTools.TextCompatibleStrict:
        """
        the self.html value auto-converted to text
        """
        return self.html.text
    @text.setter
    def text(self,text:htmlTools.TextCompatible):
        self.html=htmlTools.asText(text).html
