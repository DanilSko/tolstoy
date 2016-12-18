from bs4 import BeautifulSoup as BS
import re, string, os

##html_doc = """
##<html><head><title>The Dormouse's story</title></head>
##<body>
##<p class="title"><b>The Dormouse's story</b></p>
##
##<p class="story">Once upon a time there were three little sisters; and their names were
##<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
##<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
##<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
##and they lived at the bottom of a well.
##<a href="http://example.com/tillie" class="sister" id="link4">Tillie
##</a>здесь кириллица.: - \n\t- at the bottom of a well.: - \n\t- .<div id="div1">some text</div>
##</p>
##
##<p class="story">...</p>
##"""
##
##print(string.punctuation)
##regexp = '[\w ]+$'
##soup = BS(html_doc, 'lxml-xml')
##
##for tag in soup.find_all(True):
##    if tag.name == 'div':
##        sib = tag.previous_sibling
##        sib = sib.strip(string.punctuation+' \t\n')
##        
##        print(sib)

##string = 'abcdef'
##print(string[1:4])
##
##string = 'î'
##print(ord(string))

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


##def print_latin(text, indexL, indexR):
##    print(text[0:indexL])
##    print('____________')
##    print(text[indexL:indexR])
##    print('____________')
##    print(text[indexR:])
##    print('************')


def return_romanCharNums():
    nums = []
    nums.extend(list(range(65, 91)))
    nums.extend(list(range(97, 123)))
    nums.extend([138,140,142,154,156,158,159])
    nums.extend(list(range(192, 256)))
    nums = set(nums)
    return nums
        
    
def check_for_roman_numbers(text, romanCharNums):
    romanNumChars = set('IVXMCDivxmcd')
    isnotRomanNum = False
    for i in range(len(text)):
        i = 0 - (1+i)
        if ord(text[i]) not in romanCharNums:
            break
        elif text[i] not in romanNumChars:
            isnotRomanNum = True
    return isnotRomanNum
        

##def search_for_indexes(text, romanCharNums):
##    romanCharNums = set(range(0, 256))
##    indexR = 0
##    indexL = 0
##    for i in range(len(text)):
##        i = 0 - (1+i)
##        if not ord(text[i]) in romanCharNums:
##            if indexR == 0:
##                indexR = i
##        if ord(text[i]) in set(range(1024, 1280)):
##            indexL = i
##            break
##    return indexL, indexR


def print_latin_2(text, index):
    print(text[:index])
    print('____________')
    print(text[index:])
    print('************')
    
    
def search_for_indexes_2(text):
    index = 0
    for i in range(len(text)):
        i = 0 - (i+1)
        if ord(text[i]) in set(range(1024, 1280)):
            index = i+1
            break
    return index

    
##def search_for_latin(text, romanCharNums):
##    indexL, indexR = search_for_indexes(text, romanCharNums)
##    print_latin(text, indexL, indexR)
    

def search_for_x(text, d):
    index = search_for_indexes_2(text)
    latinText = text[index:]
    latinText = latinText.strip(' ')
    arr = latinText.split(' ')
    el = arr[0]
##    if el == '—':
##        print(latinText)
    d = make_dict(d, el)
    return d

    
def search_for_latin_2(text):
    index = search_for_indexes_2(text)
##    print_latin_2(text, index)
    return text[index:]


def search_for_types(tag):
    tagType = ''
    for innerTag in tag.find_all(True):
        tagType += innerTag.name+' '
    return tagType[:-1]


def print_set(someSet):
    for el in someSet:
        print(el)
    print('_______________')


def make_dict(d, key):
    if not key in d:
        d[key] = 1
    else:
        d[key] += 1
    return d


def print_dict(d):
    for key in sorted(d):
        print(key+' - '+str(d[key]))
    

##def print_attrs(tag):
##    for innerTag in tag.find_all(True):
##        if innerTag.name == 'hi':
##            for key in innerTag.attrs:
##                print(key)

def make_table(table, trans, orig, path, n):
    table += trans+'\t'+orig+'\t'+path+'\t'+n+'\n'
    return table

    
def main():
    table = 'trans\torig\tpath\tn\n'
    romanCharNums = return_romanCharNums()
    pathes = walker('add_del')
    counter = 0
    types = {}
    d = {}
    for path in pathes:
        xml = f_read(path)
        soup = BS(xml, 'lxml-xml')
        for tag in soup.find_all(True):
            if tag.name == 'lb':
                tag.unwrap()
        for tag in soup.find_all(True):
            if tag.name == 'note':
                sibling = tag.previous_sibling
                if 'String' in str(type(sibling)):
                    s = sibling.strip(string.punctuation+' \t\n—'+\
                                      '0123456789')
                    if not len(s) == 0:
                        if ord(s[-1]) in romanCharNums:
                            isnotRomanNum =\
                                          check_for_roman_numbers(s,
                                                                  romanCharNums)
                            if isnotRomanNum is True:
                                tagType = search_for_types(tag)
##                                types = make_dict(types, tagType)
                                if tagType == 'div head ref p':
                                    translation = tag.p.string
                                    translation = translation.strip()
                                    if not translation.startswith('['):
                                        n = tag['n']
                                        latin = search_for_latin_2(s)
                                        table = make_table(table, translation,
                                                           latin, path, n)
##                                        print(table)

##                                    print(translation.string)
####                                    print_attrs(tag)
##                                    
##                                    print(path)
##                                    print(tag)
##                                    print('**********')
                                    

##                                    search_for_x(s, d)
                                        counter += 1
                                
    print(counter)
    f_write('table_resp_author.csv', table)
##    print_dict(d)
                       
        
    
            
main()        
