import re
import urllib.request

def web():
    req = urllib.request.Request('http://vpered-balezino.ru/')
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    return(html)

def articles():
    html = web()
    art_reg = re.compile('<h3.*?</h3>', flags= re.DOTALL)
    art = art_reg.findall(html)
    return(art)

def write():
    art = articles()
    tags_reg = re.compile('<.*?>', re.DOTALL)
    spaces_reg = re.compile('\s{2,}', re.DOTALL)
    with open('articles.txt', 'w', encoding = 'utf-8') as m:
        for a in art:
            a = spaces_reg.sub("", a)
            a = tags_reg.sub("", a)
            m.write(a + '\n')

web()
articles()
write()
