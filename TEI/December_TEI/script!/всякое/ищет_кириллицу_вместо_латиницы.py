from bs4 import BeautifulSoup as BS
import re, string, os

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


def return_romanCharNums():
    nums = []
    nums.extend(list(range(65, 91)))
    nums.extend(list(range(97, 123)))
    nums.extend([138,140,142,154,156,158,159])
    nums.extend(list(range(192, 256)))
    nums = set(nums)
    return nums


def process_text(text, latin, cyrillic, path):
    for i in range(len(text)):
        if ord(text[i]) in latin:
            if i+1 < len(text):
                if ord(text[i+1]) in cyrillic:
                    print(path)
                    print(text[i])
                    print(text[i+1])
                    print('********')
        elif ord(text[i]) in cyrillic:
            if i+1 < len(text):
                if ord(text[i+1]) in latin:
                    print(path)
                    print(text[i])
                    print(text[i+1])
                    print('********')

    
def main():
    latin = return_romanCharNums()
    latin.remove(105)
    print(latin)
    cyrillic = set(range(1024, 1280))
    pathes = walker('add_del')
    for path in pathes:
        xml = f_read(path)
        soup = BS(xml, 'lxml-xml')
        body = soup.find('text')    
        text = body.get_text()
        process_text(text, latin, cyrillic, path)


main()



        
