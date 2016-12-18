##берет файл html и переводит его в tei, меняя хедер. Хедер берет из файла
##tei_header.txt.

import codecs, re, os
from bs4 import BeautifulSoup
from bs4 import diagnose


def f_read(filename):
    f = open(filename, 'r', encoding = 'utf-8-sig')
    text = f.read()
    f.close()
    return text


def f_write(filename, text):
    f = open(filename, 'w', encoding = 'utf-8-sig')
    f.write(text)
    f.close()

    
def attrs(name, value):
    if name == 'style':
        newName = 'style'
    elif name == 'class':
        newName = 'rend'
    elif name == 'id':
        newName = 'xml:id'
    elif name == 'href':
        newName = 'target'        
    elif name == 'src':
        newName = 'url'
    elif name == 'border':
        newName = 'style'
        value = 'border:'+value
    elif name == 'valign':
        newName = 'style'
        value = 'vertical-align:'+value
    elif name == 'width':
        newName = 'style'
        value = 'width:'+value
    elif name == 'colspan':
        newName = 'rend'
        value = 'colspan:'+value
    elif name == 'rowspan':
        newName = 'rend'
        value = 'rowspan:'+value
    elif name == 'alt':
        newName = 'rend'
        value = 'alt:'+value
    elif name == 'type':
        newName = 'style'
        value = 'type:'+value

    elif name == 'style':#если попадется второй раз
        newName = 'style'
    elif name == 'rend':
        newName = 'rend'
    elif name == 'n':
        newName = name
    elif name == 'xml:id':
        newName = name
    return newName, value

##принимает имя тега html,
##возвращает имя соответствующего ему тега tei
def tags(tagname):
    attrname = ''
    attrvalue = ''
    if tagname == 'body':
        newTagname = 'body'
    elif tagname == 'p':
        newTagname = 'p'
    elif tagname == 'h1' or tagname == 'h2' or tagname == 'h3' \
         or tagname == 'h4' or tagname == 'h5' or tagname == 'h6':
        newTagname = 'head'
    elif tagname == 'a':
        newTagname = 'ref'
    elif tagname == 'table':
        newTagname = 'table'
    elif tagname == 'tr':
        newTagname = 'row'
    elif tagname == 'td':
        newTagname = 'cell'
    elif tagname == 'div':
        newTagname = 'div'
    elif tagname == 'col':
        newTagname = 'col'
    elif tagname == 'br':
        newTagname = 'lb'
    elif tagname == 'em':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'em'
    elif tagname == 'strong':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'strong'
    elif tagname == 'sup':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'sup'
    elif tagname == 'i':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'i'
    elif tagname == 'span':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'span'
    elif tagname == 'sub':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'sub'
    elif tagname == 'colgroup':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'colgroup'
    elif tagname == 'hr':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'hr'
    elif tagname == 'tbody':
        newTagname = 'hi'
        attrname = 'rend'
        attrvalue = 'tbody'
    elif tagname == 'img':
        newTagname = 'graphic'
    elif tagname == 'choice':
        newTagname = tagname
    elif tagname == 'reg':
        newTagname = tagname
    elif tagname == 'orig':
        newTagname = tagname
    elif tagname == 'note':
        newTagname = tagname
    elif tagname == 'pb':
        newTagname = tagname
    elif tagname == 'viii':#левый тег
        newTagname = tagname
    elif tagname == 'head':#левый тег
        newTagname = 'head?'
    return newTagname, attrname, attrvalue


def process(tag, soup):
    tagName, attrName, attrValue = tags(tag.name)
    newTag = soup.new_tag(tagName)
    if len(attrName) > 0:
        newTag[attrName] = attrValue
    for key in tag.attrs:
        attrName, attrValue = attrs(key, tag[key])
        if attrName in newTag:
            if attrName == 'style':
                sep = '; '
            elif attrName == 'rend':
                sep = ' '
            else:
                print('Некоторый (не style и rend) атрибут встретился дважды!')
            newTag[attrName] += sep+attrValue
        else:
            newTag[attrName] = attrValue
    tag.name = newTag.name
    tagAttrs = []
    for key in tag.attrs:
        tagAttrs.append(key)
    for attr in tagAttrs:
        del tag[attr]
    for key in newTag.attrs:
        tag[key] = newTag[key]
    if tag.name == 'graphic':
        tag.wrap(soup.new_tag('figure'))


def walker(path):
    pathes = []
    for root, dirs, files in os.walk(path):
##        print(root)
        for filename in files:
            if filename.endswith('xml'):
                path = filename
                pathes.append(path)
    return pathes


def process_doc(fnameSource, fnameGoal):
    text = f_read(fnameSource)
    soup = BeautifulSoup(text, 'lxml-xml')
    body = soup.find('text')
    allTags = body.find_all(True)
    for tag in allTags:
        try:
            if tag.name == 'viii':
                print('viii - '+fnameSource)
            elif tag.name == 'head':
                print('head - '+fnameSource)            
            process(tag, soup)
        except UnboundLocalError:
            print('local error')
            print(tag.name)
    f_write(fnameGoal, soup.prettify())
    

def main(directory):
    pathSource = os.path.join('..', directory)
    pathGoal = os.path.join('..', 'Volumes9to12_18to19_converted')
    if not os.path.exists(pathGoal):
        os.mkdir(pathGoal)
    filenames = walker(pathSource)
    print(len(filenames))
    for filename in filenames:
        fnameSource = os.path.join(pathSource, filename)
        fnameGoal = os.path.join(pathGoal, filename)
        process_doc(fnameSource, fnameGoal)
    print('done')

main('Volumes9to12_18to19')
    
    




