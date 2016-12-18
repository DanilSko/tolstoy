import os#, re
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


def read_split(filename):
    text = f_read(filename)
    text = text.strip().split('\n')
    return text


def walker(dirName):
    pathes = []
    fNames = []
    fNamesNotProcessed = []
    for root, dirs, files in os.walk(os.path.join('..',
                                                  dirName)):
        for filename in files:
            if filename.endswith('xml'):
                path = os.path.join(root, filename)
                pathes.append(path)
                fNames.append(filename)
            else:
                fNamesNotProcessed.append(filename)
    return pathes, fNames, fNamesNotProcessed


def combine_gdemal(gdemala, gdemalb):
    gdemal = []
    for worda in gdemala:
        for wordb in gdemalb:
            word = worda+' '+wordb
            gdemal.append(word)
    return gdemal


def combine_gdemalv(gdemalv):
    gdemalvCombined = []
    for worda in gdemalv:
        for wordb in gdemalv:
            gdemalvCombined.append(worda+' и '+wordb)
    gdemalv.extend(gdemalvCombined)
    return gdemalv


def load_files():
    naPolyah = 'на полях'
    napisano = read_split('.\\для парсера\\написано.txt')
    zacherknuto = read_split('.\\для парсера\\зачеркнуто.txt')
    gdebol = read_split('.\\для парсера\\гдебол.txt')
    gdemala = read_split('.\\для парсера\\гдемала.txt')
    gdemalb = read_split('.\\для парсера\\гдемалб.txt')
    gdemal = combine_gdemal(gdemala, gdemalb)
    gdemalv = read_split('.\\для парсера\\гдемалв.txt')
    gdemalv = combine_gdemalv(gdemalv)
    pozdneeWords = read_split('.\\для парсера\\позднее.txt')
    tagWords = []
    tagWords.extend(napisano)
    tagWords.extend(zacherknuto)
    tagWords.append('на полях')
    attrWords = []
    attrWords.extend(gdebol)
    attrWords.extend(gdemal)
    attrWords.extend(gdemalv)
    attrWords.append('на полях')
    return tagWords, attrWords, pozdneeWords, naPolyah, gdebol, gdemal,\
           gdemalv, napisano, zacherknuto


def normalize_kursiv(kursiv):
    kursiv = kursiv.lower()
    kursiv = kursiv.strip(': <\r\n')
    return kursiv


def find_kursiv(tag):
    def tag_name_is_hi_and_attr_value_is_em(tag):
        return tag.name == 'hi' and tag['rend'] == 'em'
    kursiv = tag.find(tag_name_is_hi_and_attr_value_is_em)
    kursiv = kursiv.get_text()
    return kursiv

##    
##def preprocess(tag, tagWords, attrWords, pozdneeWords):
##    def tag_name_is_hi_and_attr_value_is_em(tag):
##        return tag.name == 'hi' and tag['rend'] == 'em'    
##    kursiv = tag.find(tag_name_is_hi_and_attr_value_is_em)
##    kursiv = kursiv.get_text()
##    kursiv = normalize_kursiv(kursiv)
##    for word in tagWords:
##        kursiv = kursiv.replace(word, '', 1)
##    for word in attrWords:
##        kursiv = kursiv.replace(word, '', 1)
##    for word in pozdneeWords:
##        kursiv = kursiv.replace(word, '', 1)
##    kursiv = kursiv.strip(' .')
##    kursiv = kursiv.replace('\r\n', '')
##    return kursiv
        

def search_for_one_kursiv_tag(tag):
    string = ''
    oneKursiv = False
    counterHi = 0
    if tag.name == 'note':
        for innerTag in tag.find_all(True):
            if not innerTag.name == 'choice'\
               and not innerTag.name == 'reg'\
               and not innerTag.name == 'orig':
                string += innerTag.name+' '
            if innerTag.name == 'hi' and innerTag['rend'] == 'em':
                counterHi += 1
        if counterHi == 1:
            oneKursiv = True
    return oneKursiv, string
    
    
##def search_for_direct_string(tag, regexp):
##    for innerTag in tag.find_all(True):
##        if innerTag.name == 'div' or innerTag.name == 'head'\
##           or innerTag.name == 'ref':
##            for child in innerTag.find_all(string=True, recursive=False):
####                child = regexp.sub('', child)
##                child = child.strip(' \n')
##                if not len(child) == 0:
##                    print(innerTag.name)
##                    print(child)
##                    print('___________')
##


def return_tag(word, soup, pozdneeWords, napisano=[], zacherknuto=[],
               naPolyah='на полях'):
##    print(pozdneeWords)
    if word in napisano or word == naPolyah or word in pozdneeWords:
        tag = soup.new_tag('add')
    elif word in zacherknuto:
        tag = soup.new_tag('del')
    return tag


def return_attr(word, tag, naPolyah, pozdneeWords, gdebol, gdemal, gdemalv):
    if word in naPolyah or word in gdemal or word in gdemalv\
       or word in pozdneeWords:
        if 'place' not in tag.attrs:
            tag['place'] = word
        else:
            tag['place'] += '; '+word
    elif word in gdebol:
        if 'stage' not in tag.attrs:
            tag['stage'] = word
        else:
            tag['stage'] += '; '+word
    return tag


def process_notes(kursiv, soup, tagWords, attrWords, pozdneeWords, naPolyah,
                  gdebol, gdemal, gdemalv, napisano, zacherknuto):
    kursiv = normalize_kursiv(kursiv)
    for word in pozdneeWords:
        kursiv = kursiv.replace(word, '')
    if kursiv == naPolyah or kursiv in gdebol or kursiv in gdemal\
       or kursiv in pozdneeWords or kursiv in gdemalv:
        newTag = process_attr_tags(kursiv, soup, naPolyah, gdebol,
                                    gdemal, pozdneeWords, gdemalv)
        kursiv = ''
    else:
        for word in tagWords:
            if word in kursiv:
                kursiv = kursiv.replace(word, '', 1)
                newTag = return_tag(word, soup, pozdneeWords, napisano,
                                    zacherknuto, naPolyah)
                break
        if not 'newTag' in locals():
            for word in pozdneeWords:
                kursiv = kursiv.replace(word, '', 1)
                newTag = return_tag(word, soup, pozdneeWords)
                break
        if 'newTag' in locals():
            for word in attrWords:
                if word in kursiv:
                    kursiv = kursiv.replace(word, '', 1)
                    newTag = return_attr(word, newTag, naPolyah, pozdneeWords,
                                         gdebol, gdemal, gdemalv)
    return newTag, kursiv
    

def process_attr_tags(word, soup, naPolyah, gdebol, gdemal, pozdneeWords,
                      gdemalv):
    tag = soup.new_tag('add')
    tag = return_attr(word, tag, naPolyah, pozdneeWords, gdebol, gdemal,
                      gdemalv)
##    print(5)
    return tag


##def delete_empty_tags(newTag, path, kursiv):
##    allTags = newTag.find_all(True)
##    for tag in allTags:
##        content = tag.contents
##        if content is None:
##            print('None')
####        print(len(content))
##        if len(content) == 1:
##            print(tag)
####            print(type(content[0]))
##            if 'string' in str(type(content[0])):
##                print('!!!!!!!!')
##                print(path)
##                print(tag.name)
##                print(content[0])
##                print(kursiv)
##                print('_____________')
    
    
    
    
##def convert_oldTag_into_newTag(soup, oldTag, newTag):
####    print(soup.oldTag)
##    oldTag.wrap(newTag)
##    print(newTag)


def newTag_process(newTag, path, kursiv):
    idNo = newTag.note['n']
    newTag['n'] = idNo
    tags = newTag.find_all(True)
    for tag in tags:
        if tag.name == 'div' or tag.name == 'head' or tag.name == 'ref':
            for child in tag.find_all(string=True, recursive=False):
                child.replace_with('')
            tag.unwrap()
        elif tag.name == 'note':
            tag.unwrap()
        elif tag.name == 'hi' and tag['rend'] == 'em':
            tag.decompose()
    return newTag
    
def main():
    resultDir = os.path.join('..', 'add_del')
    if not os.path.exists(resultDir):
        os.mkdir(resultDir)
##    regexp = re.compile('\d+', flags=re.U|re.DOTALL)
    tagWords, attrWords, pozdneeWords, naPolyah, gdebol, gdemal,\
           gdemalv, napisano, zacherknuto = load_files()
    pathes, fNames, fNamesNotProcessed = walker('converted')
    counterP = 0
    counterNP = 0
    types = set()
    fNamesIndex = 0
    for path in pathes:
        text = f_read(path)
        soup = BS(text, 'lxml-xml')
        body = soup.find('text')
        tags = body.find_all(True)
        for tag in tags:
            oneKursiv, string = search_for_one_kursiv_tag(tag)
            if oneKursiv:
                kursiv = find_kursiv(tag)
                newTag, kursiv = process_notes(kursiv, soup, tagWords,
                                               attrWords,
                                       pozdneeWords,
                              naPolyah, gdebol, gdemal, gdemalv, napisano,
                              zacherknuto)
                if len(kursiv) == 0:
                    tag.wrap(newTag)
                    newTag = newTag_process(newTag, path, kursiv)
##                    if newTag.name == 'del':
##                        print(path)
##                        print(newTag)
                    counterP += 1
                else:
                    counterNP += 1
        f_write(os.path.join(resultDir, fNames[fNamesIndex]), soup.prettify())
        fNamesIndex += 1
    print(counterP)
    print(counterNP)
                
              
                
def print_set(someSet):
    for el in sorted(someSet):
        print(el)
    print('_______________')                


main()

