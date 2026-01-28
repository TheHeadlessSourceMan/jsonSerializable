
def convertToLinks(text):
    """
    Attempts to find all links in a piece of html and convert them into clickable items.
    """
    text=text+'\n' # must end in newline for this regex to work
    import re
    # Convert all links
    pattern=re.compile(r"""([>\s])(\w+://[^<\s]+)([<\s])""")
    for url in re.finditer(pattern,text):
        text=text[0:url.start(2)]+'<a href="'+url.group(2)+'">'+url.group(2)+'</a> '+text[url.end(2):]
    # Convert all email addresses
    pattern=re.compile(r"""([>\s])([_\.\w]+@[_\.\w])+([<\s])""")
    for url in re.finditer(pattern,text):
        text=text[0:url.start()]+'<a href="mailto://'+url.group().strip()+'">'+url.group()+'</a> '+text[url.end():]
    return text[0:-1]


def tidy(self,saveIt:bool=True)->bool:
    """
    Tidy up the output using html tidy (if installed).
    (see http://tidy.sourceforge.net)
    """
    cmd='tidy --input-xml 1 --indent 1 --quiet 1 --output-xhtml 1 --write-back 1 '+self.project.fileFull
    _,err=subprocess.Popen(cmd,stderr=subprocess.PIPE).communicate()
    if err:
        print(err)
        return False
    return True


def guessIsHtml(text,preferHtml=True):
    """
    preferHtml - if there's a debate, prefer to assume html over not (pretty safe to do, really)
    """
    if type(text)!=str:
        return False
    import re
    quickList=['a','div','pre','br','hr','span','u','b','p','td','img','embed'] # not exhaustive, but effective
    isHtml=False
    pattern=re.compile(r"""<([/_\w]+)[^>]*>""")
    count=0
    for tagname in re.finditer(pattern,text):
        if tagname in quickList:
            isHtml=True
            break
        elif count>0 and preferHtml:
            # since there's more than one tag, even though it's unrecognized, let's accept it
            isHtml=True
            break
        else:
            count=count+1
    return isHtml


def deleteAllChildNodes(domElement):
    while domElement.hasChildNodes():
        domElement.removeChild(domElement.firstChild)


def getDocumentFor(domElement):
    """
    The documentation says this should work.
    The documentation lies.
    """
    while domElement.parentNode is not None:
        domElement=domElement.parentNode
    return domElement


def getInnerHtml(domElement):
    return domElement.toxml().split('>',1)[-1].rsplit('<',1)[0]


def setInnerHtml(domElement,newHtml,appendToExisting:bool=False):
    import xml.dom.minidom
    if not appendToExisting:
        deleteAllChildNodes(domElement)
    newHtml='<simprini>'+newHtml+'</simprini>'
    try:
        docFrag=xml.dom.minidom.parseString(newHtml)
        for node in docFrag.firstChild.childNodes:
            domElement.appendChild(node.cloneNode(True))
        docFrag.unlink()
    except xml.parsers.expat.ExpatError as e:
        print(e)
        newHtml=newHtml[10:-11]
        print(newHtml)