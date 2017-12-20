from bs4 import BeautifulSoup
import urllib.request
from urllib import parse
import re
import os
import shutil
from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import sqlite3
import html

#сделать переводчик
#изменить функцию с 10 словами

app = Flask(__name__)

#создание главной страницы и вывод на экран погоды в Скопье
@app.route('/')
def weather():
    user = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request('https://www.gismeteo.ru/weather-skopje-3253/', headers={'User-Agent':user})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('ISO-8859-1')

    reg = re.compile('<span class="js_value tab-weather__value_l">(\s.*?)<span class="tab-weather__value_m">', re.DOTALL) 
    reg_2 = re.compile('<span class="tab-weather__feel-value">(\s.*?)<', re.DOTALL)
    weather_dirty = re.search(reg, html).group(1)

    if re.search('&minus;', weather_dirty):
        weather = re.sub('&minus;', '-', weather_dirty)
    else:
        weather = weather_dirty
    
    weather_feel_dirty = re.search(reg_2, html).group(1)
    
    if re.search('&minus;', weather_feel_dirty):
        weather_feel = re.sub('&minus;', '-', weather_feel_dirty)
    else:
        weather_feel = weather_feel_dirty
    
    return render_template("main.html", weather = weather, weather_feel = weather_feel)

#создание словаря дореволюционных слов
def dictionary():
    user = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    URL = 'http://www.dorev.ru/ru-index.html?l='
    req = urllib.request.Request(URL, headers={'User-Agent':user})
    reg_ends = re.compile(r'<a href="ru-index\.html\?l=([cd][0-9]|[cd][a-f])"><b class="uu">', re.DOTALL)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows-1251')
    ends = []
    ends = re.findall(reg_ends, html)
    dorev = {}
    reg_whole = re.compile(r'(<td class="uu">([А-Яа-яЁёёѣѳѵі]{2,})<\/td><td>)(<\/td><td class="uu">([А-Яа-яЁё&#0-9A-Za-z;]+)*?<span class="u0">)(<span class="u1">([а-яё&#0-9a-z;]+)<\/span>)(<span class="u[2-5]">.<\/span><\/span>([а-яё&#0-9a-z;]+)[\s|<\/td>|,])', re.DOTALL)
    reg_words = re.compile(r'<td class="uu">([А-Яа-яЁёёѣѳѵі]{2,})<\/td><td>', re.DOTALL)
    reg_dorev_1 = re.compile(r'<\/td><td class="uu">([А-Яа-яЁё&#0-9A-Za-z;]+)*?<span class="u0">', re.DOTALL)
    reg_dorev_2 = re.compile(r'<span class="u1">([а-яё&#0-9a-z;]+)<\/span>', re.DOTALL)
    reg_dorev_3 = re.compile(r'<span class="u[2-5]">.<\/span><\/span>([а-яё&#0-9a-z;]+)[\s|<\/td>|,]', re.DOTALL) 
    links = []
    htmls = []
    whole = []
    for i in ends:
        links = URL + str(i)
        htmls = read_htmls(links, user)
        if htmls != '': 
            whole = re.findall(reg_whole, htmls)
            for i in whole:
                new_list = re.findall(reg_words, i[0])
                new = ''.join(new_list)
                first_list = re.findall(reg_dorev_1, i[2])
                first = ''.join(first_list)
                second_list = re.findall(reg_dorev_2, i[4])
                second = ''.join(second_list)
                third_list = re.findall(reg_dorev_3, i[6])
                third = ''.join(third_list)
                old = first + second + third
                dorev[new] = old
    json.dump(dorev, open('dict.json', 'w', newline=''))         

def read_htmls(links, user):
    try:
        req2 = urllib.request.Request(links, headers={'User-Agent':user})
        with urllib.request.urlopen(req2) as response:
            htmls = response.read().decode('windows-1251')
        return htmls
    except:
        print = 'Страница не найдена'
        htmls = ''
        return htmls

#перевод слова в дореволюционную орфографию
@app.route('/dorev')
def translated_word():
    vowels = ['у', 'У', 'е', 'Е', 'ы', 'Ы', 'а', 'А', 'о', 'О', 'э', 'Э', 'я', 'Я', 'и', 'И', 'ю', 'Ю', 'ё', 'Ё', 'й', 'Й']
    consonants = ['ц', 'Ц', 'к', 'К', 'н', 'Н', 'г', 'Г', 'ш', 'Ш', 'щ', 'Щ', 'з', 'З', 'х', 'Х', 'ф', 'Ф', 'в', 'В', 'п', 'П', 'р', 'Р', 'л', 'Л', 'д', 'Д', 'ж', 'Ж', 'ч', 'Ч', 'с', 'С', 'м', 'М', 'т', 'Т', 'б', 'Б']
    with open('dict.json', "r", encoding = 'utf-8') as f: 
        dorev = json.load(f)
    word = request.args['word']
    for key in dorev:
        if word == key:
            word = dorev[key]
        else:
            for l in range(len(word)):
                if word[l-1] == 'и' and word[l] in vowels:
                    word = word[:l-1] + 'i' + word[l:]
                if word[l-1] == 'И' and word[l] in vowels:
                    word = word[:l-1] + 'I' + word[1:]
            for i in consonants:
                if word.endswith(i):
                    word += 'ъ'
            if word.startswith('бес'):
                word = re.sub('бес', 'без', word)
            if word.startswith('черес'):
                word = re.sub('черес', 'через', word)
            if word.startswith('чрес'):
                word = re.sub('чрес', 'чрез', word)
    word = html.unescape(word)
    return render_template('dorev.html', word = word)
        
@app.route('/news')
def input_link():
    return render_template('news.html')

#грузит эту страницу 200 лет (минут 10) (((((((( ничего не могу поделать, извините
@app.route('/site')
def site():
    link = request.args['ссылка']
    text = translated_text(link)
    return render_template('site.html', text = text)

def translated_text(link):
    user = 'Google Chrome/61.0 (Windows NT 6.1; Win64; x64)' 
    req = urllib.request.Request(link, headers={'User-Agent':user}) 
    with urllib.request.urlopen(req) as html: 
        html = html.read().decode('utf-8')
    dirty = BeautifulSoup(html, 'html.parser')
    text = dirty.get_text()
    cyril = re.findall('[А-Яа-яЁё]{2,}', text)
    clean = ' '.join(cyril)
    text = re.sub('\s{2,}', ';', clean) 
    text = text.lower()
    text = text.split()
    vowels = ['у', 'У', 'е', 'Е', 'ы', 'Ы', 'а', 'А', 'о', 'О', 'э', 'Э', 'я', 'Я', 'и', 'И', 'ю', 'Ю', 'ё', 'Ё', 'й', 'Й']
    consonants = ['ц', 'Ц', 'к', 'К', 'н', 'Н', 'г', 'Г', 'ш', 'Ш', 'щ', 'Щ', 'з', 'З', 'х', 'Х', 'ф', 'Ф', 'в', 'В', 'п', 'П', 'р', 'Р', 'л', 'Л', 'д', 'Д', 'ж', 'Ж', 'ч', 'Ч', 'с', 'С', 'м', 'М', 'т', 'Т', 'б', 'Б']
    with open('dict.json', "r", encoding = 'utf-8') as f: 
        dorev = json.load(f)
    tr_text = ''
    for word in text:
        for key in dorev:
            if word == key:
                word = dorev[key]
            else:
                for i in consonants:
                    if word.endswith(i):
                        word += 'ъ'
                if word.startswith('бес'):
                    word = re.sub('бес', 'без', word)
                if word.startswith('черес'):
                    word = re.sub('черес', 'через', word)
                if word.startswith('чрес'):
                    word = re.sub('чрес', 'чрез', word)
                for l in range(len(word)):
                    if word[l-1] == 'и' and word[l] in vowels:
                        word = word[:l-1] + 'i' + word[l:]
                    if word[l-1] == 'И' and word[l] in vowels:
                        word = word[:l-1] + 'I' + word[1:]
            #тут почему-то не работало html.unescape (((((((
##            if re.search('&#1110;', word):
##                word = re.sub('&#1110;', 'i', word)
##            if re.search('&#1030;', word):
##                word = re.sub('&#1030;', 'І', word)
##            if re.search('&#1123;', word):
##                word = re.sub('&#1123;', 'ѣ', word)
##            if re.search('&#1139;', word):
##                word = re.sub('&#1139;', 'ѳ', word)
##            if re.search('&#1038;', word):
##                word = re.sub('&#1038;', 'Ѳ', word)
##            if re.search('&#1141;', word):
##                word = re.sub('&#1141;', 'ѵ', word)
        tr_text += word + ' '
    return tr_text  

#тест на знание старой орфографии    
@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

@app.route('/after')
def checking():
    answers = dict(request.args)
    wrong = ''
    k = 0
    for a in answers:
        if answers[a][0] == '0':
            k+= 1
            if wrong == '':
                wrong = wrong + a
            else:
                wrong = wrong + ',' + a
    if k == 0:
        results = 'Поздравляем! Вы ответили правильно на все 10 вопросов.'
    else:
        results = 'Вы ответили правильно на ' + str(10 - k) + ' из 10 вопросов. Вы ошиблись в вопросе(ах) под номером(ами): ' + wrong + '.'
    return render_template('after.html', results = results)

    
if __name__ == '__main__':
    app.run(debug=True)
    
