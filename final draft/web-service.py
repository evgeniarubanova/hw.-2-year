import re
import urllib.request  
import pymystem3
from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
import flask
from flask import url_for, render_template, request, redirect
from flask import Flask

reg_tag = re.compile('<.*?>', re.DOTALL)
reg_space = re.compile('\s{2,}', re.DOTALL)
reg_scripts = re.compile('<script.*?<\/script>', re.DOTALL)
reg_imgs = re.compile('<img src=".*?>', re.DOTALL)
reg_n = re.compile('(\n)+', re.DOTALL)
reg_hr = re.compile('<hr', re.DOTALL)
reg_clean = '[\.\?!"@—№;%:?*_()-+=#«»$-^&:;\'"><,/\|\\~`•]'

morph = MorphAnalyzer()

def collect_urls():
    common_URL = 'http://vse-shutochki.ru/anekdoty/'
    urls = []
    for i in range(1,1125):
        if i == 1:
            URL = common_URL
            urls.append(URL)
        else:
            URL = common_URL + str(i)
        with open('urls.txt', 'a', encoding = 'utf-8') as u:
            u.write(URL + '\n')

def collect_htmls():
    urls = open('urls.txt', 'r', encoding = 'utf-8')
    user = 'Google Chrome/61.0 (Windows NT 6.1; Win64; x64)'
    for url in urls:
        page = urllib.request.Request(url, headers={'User-Agent':user})
        with urllib.request.urlopen(page) as p:
            html = p.read().decode('utf-8')
            html = reg_space.sub(" ", html)
            html = reg_n.sub(' ', html)
            with open('htmls.txt', 'a', encoding = 'utf-8') as h:
                h.write(html + '\n')

def find_texts():
    reg = re.compile('<div class="post">(\S.*?)<hr', re.DOTALL)
    htmls = open('htmls.txt', 'r', encoding = 'utf-8')
    for html in htmls:
        if re.search(reg, html):
            text = re.findall(reg, html)
            for i in text:
                i = reg_scripts.sub('', i)
                i = reg_imgs.sub('', i)
                i = reg_tag.sub(" ", i)
                i = reg_hr.sub(" ", i)
                i = reg_space.sub(" ", i)
                if re.search(reg_clean, i):
                    clean_text = re.sub(reg_clean, "", i)
                else:
                    text = ''
                with open('texts.txt', 'a', encoding = 'utf-8') as t:
                    t.write(i + '\n')
        
def define_character():
    anecs = open('texts.txt', 'r', encoding = 'utf-8')
    characters = []
    anec_charact = {}
    stuff = re.compile('(.*?,).*?', re.DOTALL)
    for anec in anecs:
        s = 0
        for word in anec.split():
            if re.search(stuff, word):
                word = re.sub(stuff, '', word)
            else:
                pass
            if re.search(reg_clean, word):
                word = re.sub(reg_clean, '', word)
            else:
                pass
            ana = morph.parse(word)
            first = ana[0]
            tag = first.normalized.tag
            form = first.normalized.normal_form
            if 'NOUN' in tag and 'anim' in tag:
                s += 1
                if s == 1:
                    anec_charact.setdefault(form, [])
                    anec_charact[form].append(anec)
                    if form not in characters:
                        characters.append(form)
                    else:
                        pass
                else:
                    pass
            else:
                pass
    characters.sort()
    return characters, anec_charact

#def user():
#    characters, anec_charact = define_character()
#    user_character = input('Введите персонажа или тему анекдота, выбрав из предложенных:' + '\n' + '\n' + '\t' + str(characters)[1:-1] + '.' + '\n' + '\n')
#    print('\n')
#    if user_character in characters:
#        character = user_character 
#        for i in anec_charact[character]:
#            print(i,'************************************************')
#    else:
#        print('Попробуйте ещё раз. Выберите персонажа из списка.')
    
app = flask.Flask(__name__)

@app.route('/')
def web_1():
    characters, anec_charact = define_character()
    result = ', '.join(characters)
    return render_template('1.html', result = result)

@app.route('/response')
def web_2():
    characters, anec_charact = define_character()
    user_character = request.args['персонаж']
    if user_character in characters:
        character = user_character 
        response = anec_charact[character]
    return render_template('2.html', response = response)
    
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
#if __name__ == '__main__':
#    app.run(debug=True)

