#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Html to text and vice-versa
"""
import typing
import re


# --------------------------------------------------------

def txt2html(text:typing.Union[str,typing.Any],replaceSpaces:bool=True,replaceTabs:bool=True,replaceReturns:bool=True,
    symbolicFormatting:bool=True,createLinks:bool=True,hLevel:int=2):
    """
    Symbolic formatting (a lite form of markdown):
        _txt_ => <u>txt</u>
        *txt* => <b>txt</b>
        /txt/ => <i>txt</i>
        txt: => <h2>txt<h2>
        * txt => <li>txt</li>
        --------- => <hr />

    NOTE: Will NOT try to be clever with Html objects or object with .html members.
        Thus, txt2html(Html("<u>this</u>")) will return the escaped html "&lt;u&gt;this&lt;/u&gt;"
        just the same as txt2html("<u>this</u>") would.
    """
    if text is None:
        return ''
    if type(text)!=str:
        text=str(text)
    text=text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')
    hLevel=str(hLevel)
    if replaceTabs:
        text=text.replace('\t','     ')
    if replaceSpaces:
        text=text.replace('  ',' &nbsp;')
    if replaceReturns:
        text=text.replace('\n','<br />')
    if symbolicFormatting:
        seps=['-','=','\\*','/','#','\\~','x','X']
        text=re.sub(r"""_([^\s][^_]*)_""","""<u>\1</u>""",text)
        text=re.sub(r"""\*([^\s][^_]*)\*""","""<b>\1</b>""",text)
        text=re.sub(r"""/([^\s][^_]*)/""","""<i>\1</i>""",text)
        text=re.sub(r"""^\s*\*\s([^^]*)""","""<li>\1</li>""",text)
        text=re.sub(r"""([^:]*):\s*?\n""","""<h"""+hLevel+""">\1</h"""+hLevel+""">""",text)
        for sep in seps:
            text=re.sub(r"""\s*["""+sep+r"""]{2,9999}\s*""","""<hr />""",text)
    if createLinks:
        text=re.sub(r"""([a-zA-Z]+://[^\s]+)""","""<a href="\1">\1</a>""",text)
    return text.splitlines()[0]


def htmlEscape(text:typing.Union[str,typing.Any],replaceSpaces:bool=True,replaceTabs:bool=True,replaceReturns:bool=True,
    symbolicFormatting:bool=True,createLinks:bool=True,hLevel:int=2):
    """
    Another name for txt2html
    """
    return txt2html(text,replaceSpaces,replaceTabs,replaceReturns,
        symbolicFormatting,createLinks,hLevel)


def htmlencode(text:typing.Union[str,typing.Any],replaceSpaces:bool=True,replaceTabs:bool=True,replaceReturns:bool=True,
    symbolicFormatting:bool=True,createLinks:bool=True,hLevel:int=2):
    """
    Another name for txt2html
    """
    return txt2html(text,replaceSpaces,replaceTabs,replaceReturns,
        symbolicFormatting,createLinks,hLevel)

# --------------------------------------------------------

def html2txt(html:typing.Union[str,typing.Any]):
    """
    Capable of using (in order):
        1) BeautifulSoup
        2) nltk (old)
        3) brute force text matching (TODO: not perfect)
            does not handle special chars like &u1234;
            ignores <pre>

    See also:
        http://www.w3schools.com/tags/ref_symbols.asp
    """
    if html is None:
        return ''
    if type(html)!=str:
        html=str(html)
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        return '\n'.join(chunk for chunk in chunks if chunk)
    except ImportError:
        pass
    try:
        import nltk
        return nltk.clean_html(html) 
    except Exception:
        pass
    replacements=[
        ('  ',' '),
        ('  ',' '),
        ('&nbsp;',' '),
        ('&gt;','>'),
        ('&lt;','<'),
        ('&amp;',' ')
        ]
    ret=[]
    first=True
    ready=False
    html=html.replace('\n','').replace('\r','').replace('<br>','\n').replace('<br />','\n').replace('<br/>','\n')
    for h in html.split('<'):
        #print(h)
        if first:
            if ready:
                ret.append(h[0])
            first=False
        elif ready:
            ret.append(h.rsplit('>',1)[-1])
        elif len(h)>1 and h[1].startswith('body'):
            ready=True
    ret=' '.join(ret)
    for this,that in replacements:
        ret=ret.replace(this,that)
    return ret

def htmlUnescape(html:typing.Union[str,typing.Any]):
    """
    Another name for html2txt
    """
    return html2txt(html)

def htmldecode(html:typing.Union[str,typing.Any]):
    """
    Another name for html2txt
    """
    return html2txt(html)
    
# -----------------------------------------------

def cmdline(args):
    """
    Run the command line

    :param args: command line arguments (WITHOUT the filename)
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
                    print('ERR: unknown argument "'+arg+'"')
            else:
                print('ERR: unknown argument "'+arg+'"')
    if printhelp:
        print('Usage:')
        print('  textAndHtml.py [options]')
        print('Options:')
        print('   NONE')


if __name__=='__main__':
    import sys
    cmdline(sys.argv[1:])
