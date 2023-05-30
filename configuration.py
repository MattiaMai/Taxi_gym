'''
Configuration: abstract class containing the configuration reader
@author: Stefano Marrone
'''

import ConfigParser

class Configuration():
    def __init__(self,inifile):
        self.reader = ConfigParser.ConfigParser() 
        self.reader.read(inifile)
        self.populate()

    def genList(self,sectName,f,size):
        td = self.getSection(sectName)
        retval = map(lambda i: f(td,i),range(0,size))
        return retval

    def getSection(self,s):
        temp = dict()
        options = self.reader.options(s)
        for o in options:
            try:
                temp[o] = self.reader.get(s,o)
                if temp[o] == -1:
                    print("skip: %s" % o)
            except:
                print("exception on %s!" % o)
                temp[o] = None
        return temp
    
    def populate(self):
        pass
    
    def listFormatting(self,s):
        if (s == '-'):
            retval = None
        else:
            retval = s[1:-1]
            retval = retval.split(',')
        return retval
