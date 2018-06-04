import codecs
from lxml import etree as LXET
from os import walk #обходчик файлов

address = '../Final/'
output = 'Results/'

def filewalker (address):
    for path, dirs, filenames in walk(address):
        for filename in filename:
            parsedfile = LXET.parse ()
