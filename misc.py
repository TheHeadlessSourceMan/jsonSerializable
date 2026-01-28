"""
Misc serialization-related tools
"""
import typing
from paths import FileLocation,UrlWithLocationCompatible


def skipEmptyines(lines:typing.Union[str,typing.Iterable[str]]
    )->typing.Generator[str,None,None]:
    """
    Iterate over a series of lines, skipping empty ones
    """
    if isinstance(lines,str):
        lines=lines.replace('\r','').split('\n')
    for line in lines:
        if line:
            yield line


class StrWithFileLocation:
    """
    A string with the file location reference where it came from
    """
    def __init__(self,
        s:typing.Any,
        filename:UrlWithLocationCompatible,lineNo:int=0):
        """ """
        self.lineNo:int=lineNo
        self.filename=FileLocation(filename,fromRow=lineNo)
        if not isinstance(s,str):
            s=str(s)
        self.s=s

    def split(self,
        splitters:typing.Union[None,str]=None,
        maxSplit:typing.Optional[int]=None
        )->typing.List["StrWithFileLocation"]:
        """
        Split this string into smaller parts, each with its
        appropriate location
        """
        return [StrWithFileLocation(x,filename=self.filename,lineNo=self.lineNo)
            for x in self.s.split(splitters,maxSplit)]

    def __eq__(self,other):
        return self.s==str(other)

    def __hash__(self):
        return hash(self.s)

    def __repr__(self):
        return self.s

 # a few old things called it this.  Can probably remove pretty safely.
strWithFileLocation=StrWithFileLocation
