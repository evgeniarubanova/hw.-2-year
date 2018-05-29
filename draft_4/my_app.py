#Я долго пыталась выложить это на pythonanywhere, но тщетно. Пишет "There is a problem with your virtualenv setup.
#Look at the virtualenv section below for details". Что не так, я не знаю, делала все по инструкции.

import re
import urllib.request  
import pymystem3
from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
import flask
from flask import url_for, render_template, request, redirect
from flask import Flask
import random

reg_tag = re.compile('<.*?>', re.DOTALL)
reg_clean = '[\.\?!"@№;%:?*_()-+=#$^&:;\'"><,/\|\\~`•]'

morph = MorphAnalyzer()

def text():
    txt = []
    page = urllib.request.Request('http://ilibrary.ru/text/1005/p.1/index.html')
    with urllib.request.urlopen(page) as m:
        html = m.read().decode('windows-1251')
    text = re.sub(reg_tag, "", html)    
    text = re.sub(reg_clean, "", text)
    txt = text.split()
    return txt

def infl(user):   
    infls = []
    txt = text()
    input_txt = user.split()
    for i in input_txt:
        new_forms = []
        ana_i = morph.parse(i)[0]
        word = random.choice(txt)
        ana_rand = morph.parse(word)[0]
        
        while ana_rand.tag.POS != ana_i.tag.POS:
            if 'NOUN' in ana_i.tag.POS:
                while ana_rand.tag.gender != ana_i.tag.gender:
                    word = random.choice(txt)
                    ana_rand = morph.parse(word)[0]
            elif 'VERB' in ana_i.tag.POS:
                while ana_rand.tag.aspect != ana_i.tag.aspect:
                    word = random.choice(txt)
                    ana_rand = morph.parse(word)[0]
            else:
                word = random.choice(txt)
                ana_rand = morph.parse(word)[0]
        else:
            ana_grs = re.sub(' ', ',', str(ana_i.tag)) 
            grs = ana_grs.split(',')
            for gr in grs[1:]:
                try:
                    ana_word = ana_rand.inflect({gr})
                    if ana_word != None:
                        new_forms.append(gr)
                except:
                    pass
            for gr in new_forms:
                inf = ana_rand.inflect({gr})
        infls.append(inf.word) 
        
    string = ' '.join(infls)
    return string

app = flask.Flask(__name__)

@app.route('/page_1')
def web_1():
    return render_template('1.html')

@app.route('/page_2')
def web_2():
    data = dict(request.args)
    user = data['реплика'][0]
    string = infl(user)
    return render_template('2.html', string=string)

if __name__ == '__main__':
    app.run(debug=True)
