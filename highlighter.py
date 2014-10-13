#! /usr/bin/python

import sys
from xml import sax
from xml.sax import saxutils
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class code_getter_handler(sax.handler.ContentHandler):
    def __init__(self, outstream):
        self.targetstags = ["pre"]
        self.name = ""
        self.contents = ""
        self.out = outstream
        self.xmlGenerator = saxutils.XMLGenerator(self.out)
        
        return

    def startElement(self, name, attrs):
        self.name = name

        if self.isToBeEvaluated():
            self.out.write('<pre class="emlist highlight">')
        else:
            self.xmlGenerator.startElement(name, attrs)
            
        return
    
    def endElement(self, name):
        if len(self.contents) > 0:
            self.out.write(highlight(self.contents, PythonLexer(), HtmlFormatter(nowrap=True)))
        self.xmlGenerator.endElement(name)
        
        self.name = ""
        self.contents = ""
        
        return

    def characters(self, contents):
        if self.isToBeEvaluated():
            self.contents += contents
        else:
            self.xmlGenerator.characters(contents)
        return

    def isToBeEvaluated(self):
        return ( self.name in self.targetstags )

def main():
    #parser = sax.make_parser()

    inputStr = "<pre class=\"emlist\">import time\n" + \
               "version = release = time.strftime('%Y.%m.%d')" + \
               "</pre>"
    
    print inputStr
    sax.parseString(inputStr, code_getter_handler(sys.stdout))
    
    return


#if __name__ == "__main__":
main()
print "done..."
