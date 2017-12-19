import re
from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import sqlite3

age = {}
city = {}
language = {}
education = {}

sort_age = {}
sort_city = {}
sort_lang = {}
sort_educ = {}

app = Flask(__name__)

#страница с анкетой
@app.route('/')
def quiz():
    return render_template("form.html")

#страница, появляющаяся после заполнения анкеты
@app.route('/after')
def after():
    a = request.args['возраст']
    c = request.args['город']
    l = request.args['язык']
    e = request.args['образование']
    
    data = dict(request.args)
    
    with open('after.json', "a", newline='') as m: 
        m.write(json.dumps(data, ensure_ascii = False))

    #добавление элементов в словари

    if a not in age:
        age[a] = 1
    else:
        age[a] += 1
        
    if c not in city:
        city[c] = 1
    else:
        city[c] += 1
        
    if l not in language:
        language[l] = 1
    else:
        language[l] += 1

    if e not in education:
        education[e] = 1
    else:
        education[e] += 1

    #преобразование словарей в json
        
    json.dump(age, open('age.json', 'w', newline=''))
    json.dump(language, open('language.json', 'w', newline=''))
    json.dump(city, open('city.json', 'w', newline=''))
    json.dump(education, open('education.json', 'w', newline=''))
        
    return render_template('after.html')
    

@app.route('/stats')
def stats():

    #преобразование json в словари 
    
    age = json.load(open('age.json'))
    
    city = json.load(open('city.json'))

    language = json.load(open('language.json'))

    education = json.load(open('education.json'))

    return render_template('stats.html', age = age, city = city, language = language, education = education)

#страница с данными в формате json
@app.route('/json')
def j_son():
        
    with open('after.json', "r") as m: 
        content = m.read() 
    return render_template('json.html', content = content)

#страница с поиском
@app.route('/search')
def searching():
    return render_template('search.html')

#страница с результатами поиска
@app.route('/results')
def final():
    
    searching = request.args['search']
    with open('after.json', "r") as m: 
        content = m.read()
        
    dirty = content.split('}')
 
    rslt = []
    clean = []
    
    for i in dirty:
        cl = re.sub(r'[[|"|]|{|\]', '', i)
        clean.append(cl)
        
    for cl in clean:
        if re.search(searching, cl):
            rslt.append(cl)
            
    return render_template('results.html', rslt = rslt)  

if __name__ == '__main__':
    app.run(debug=True)
