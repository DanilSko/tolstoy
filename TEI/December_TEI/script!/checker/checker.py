import os
from bs4 import BeautifulSoup as BS

def f_read(filename):
    f = open(filename, 'r', encoding = 'utf-8-sig')
    text = f.read()
    f.close()
    return text


def f_write(filename, text, encoding = 'utf-8-sig'):
    f = open(filename, 'w', encoding = encoding)
    f.write(text)
    f.close()


def walker(dirName):
    pathes = []
    for root, dirs, files in os.walk(os.path.join('..', dirName)):
##        print(root)
        if not root.endswith('zip') and not 'MACOSX' in root:
            for filename in files:
                if filename.endswith('xml'):
                    path = os.path.join(root, filename)
                    pathes.append(path)
    return pathes

#path нужен только чтобы посмотреть, в каком тексте встречается к-нибудь тег
def return_tags_attrs(soup):
    tags = set()
    attrs = set()
    for tag in soup.find_all(True):
        tags.add(tag.name)
        for attr in tag.attrs:
            attrs.add(attr)
    return tags, attrs


def checker(tagsParser, attrsParser, tags, attrs, path):
    unknownTags = tags - tagsParser
##    if len(unknownTags) > 0:
##        print(path)
##        print_set(unknownTags)
    unknownAttrs = attrs - attrsParser
##    if len(unknownAttrs) > 0:
##        print(path)
##        print_set(unknownAttrs)
    return unknownTags, unknownAttrs
    

    
def print_set(someSet):
    for el in someSet:
        print(el)
    print('_______________')


def main():
    tagsParser = f_read('tags.txt').strip().split('\n')
    tagsParser = set(tagsParser)
    attrsParser = f_read('attrs.txt').strip().split('\n')
    attrsParser = set(attrsParser)
    pathes = walker('December_TEI_V1_no_Translit_added_Notes_added_Meta_pagebreaks')
    allUnknownTags = set()
    allUnknownAttrs = set()
    for path in pathes:
##        print(path)
        text = f_read(path)
        soup = BS(text, 'lxml-xml')
        body = soup.find('text')
        tags, attrs = return_tags_attrs(body)
        unknownTags, unknownAttrs = checker(tagsParser, attrsParser,
                                            tags, attrs, path)
        allUnknownTags |= unknownTags
        allUnknownAttrs |= unknownAttrs
    print('done')
    print_set(allUnknownTags)
    print_set(allUnknownAttrs)



main()
        
    
    
    
