import codecs, re
#from lxml import etree as LXET
from os import walk #обходчик файлов

address = '../Final/'
output = 'Results/'

header = {}
text = {}

def counter (tag, dic):
    if tag in dic:
        dic[tag]+=1
    else:
        dic[tag] =1 

def filewalker (address):
    for path, dirs, filenames in walk(address):
        for filename in filenames:
            #print (filename)
            thisdic = header
            openfile = codecs.open (path+'/'+filename, 'r', 'utf-8')
            for line in openfile:
                if '</teiHeader' in line:
                    thisdic = text
                tags = re.findall ('<([A-Za-z0-9][^\s>]*)', line)
                for tag in tags:
                    #print (tag)
                    if 'col' in tag and thisdic == text:
                        print (filename)
                    counter (tag, thisdic)
            openfile.close()
def outwriter(dct, opfilename):
    opfile = codecs.open (output+opfilename+'.csv', 'w', 'utf-8')
    for somtag in dct:
        opfile.write (somtag +'\r\n') # +';' +str(dct[somtag])+'\r\n')
    opfile.close()

filewalker (address)
outwriter(header, 'headertags')
outwriter(text, 'texttags')
print ('DONE')
                    

