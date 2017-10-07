import re
import shutil
import os
import urllib.request

#выкачка html-страниц

def read_html(URL):  
    user = 'Google Chrome/61.0 (Windows NT 6.1; Win64; x64)'
    try:
        page = urllib.request.Request(URL, headers={'User-Agent':user})
        with urllib.request.urlopen(page) as p:
            html = p.read().decode('utf-8')
        return html
    except:
        print('article ' + URL + ' does not exist')
        html = ''
        return html
    
#поиск текста в html-страницах
    
def find_text(URL):
    reg = re.compile('<div class="b-object__detail__annotation">.*?</div>.*?</div>', re.DOTALL)
    reg_tag = re.compile('<.*?>', re.DOTALL)
    reg_space = re.compile('\s{2,}', re.DOTALL)
    html = read_html(URL)
    if re.search(reg, html):
        text = re.search(reg, html).group(0)
        text = reg_space.sub(" ", text)
        text = reg_tag.sub("", text)
    else:
        text = ''
    return text

#поиск нужных данных

def data_author(URL):
    author_reg = re.compile('<span class="b-object__detail__author__name">(.*?)</span>', re.DOTALL)
    html = read_html(URL)
    if html != '':
        if re.search(author_reg, html):
            author = re.search(author_reg, html).group(1)
        else:
            author = 'Noname'
    return author

def data_header(URL):
    header_reg = re.compile('<title>(.*?) - Статьи - ', re.DOTALL)
    html = read_html(URL)
    if html != '':
        if re.search(header_reg, html):
            header = re.search(header_reg, html).group(1)
        else:
            header = 'No title'
    return header

def data_created(URL):
    created_reg = re.compile('<span class="date">(\d+\.\d+\.\d+)</span>', re.DOTALL)
    html = read_html(URL)
    if html != '':
        if re.search(created_reg, html):
            created = re.search(created_reg, html).group(1)
        else:
            created = 'Unknown'
    return created

def data_topic(URL):

    topic_reg = re.compile('<a href="/article/\?category=.*?</div>', re.DOTALL)

    reg_tag = re.compile('<.*?>', re.DOTALL)
    reg_space = re.compile('\s{2,}', re.DOTALL)
    html = read_html(URL)
    text = find_text(URL)
    if html != '':
        
        if re.search(topic_reg, html):
            topic = re.search(topic_reg, html).group(0)
            topic = reg_space.sub(" ", topic)
            topic = reg_tag.sub("", topic)
        else:
            topic = 'Unknown'
    return topic

#создание csv-таблицы

def csv(URL):
    html = read_html(URL)
    author = data_author(URL)
    header = data_header(URL)
    created = data_created(URL)
    topic = data_topic(URL)
    if re.search(r'\d+\.\d+\.(\d+)', created):
        year = re.search(r'\d+\.\d+\.(\d+)', created).group(1)
    else:
        year = 'Unknown'
    if re.search(r'\d+\.(\d+)\.\d+', created):
        month = re.search(r'\d+\.(\d+)\.\d+', created).group(1)
    else:
        month = 'Unknown'    
    path = 'newspaper/' + 'plain/' + year + '/' + month

    
    row = '%s;%s;;;%s;%s;публицистика;;;%s;;нейтральный;н-возраст;н-уровень;районная;%s;Вперёд;;%s;газета;Россия;Ульяновская область;ru'
    with open ('newspaper/metadata.csv', 'a', encoding = 'utf-8') as m:
        m.write('\n' + row%(path, author, header, created, topic, URL, year))

                    
def folders():

    os.mkdir('newspaper')
    plain = 'newspaper/plain/'
    os.mkdir(plain)
    m_xml = 'newspaper/mystem-xml/'
    os.mkdir(m_xml)
    m_plain = 'newspaper/mystem-plain/'
    os.mkdir(m_plain)
    commonURL = 'http://inza-vpered.ru/article/'
    
    #запись колонок в csv-таблицу
    
    with open ('newspaper/metadata.csv', 'w', encoding = 'utf-8') as m:
        m.write('path'+ ';' + 'author'+ ';' + 'sex'+ ';' + 'birthday'+ ';' + 'header'+ ';' + 'created'+ ';' + 'sphere'+ ';' + 'genre_fi'+ ';' + 'type'+ ';' + 'topic'+ ';' + 'chronotop'+ ';' + 'style'+ ';' + 'audience_age'+ ';' + 'audience_level'+ ';' + 'audience_size'+ ';' + 'source'+ ';' + 'publication'+ ';' + 'publisher'+ ';' + 'publ_year'+ ';' + 'medium'+ ';' + 'country'+ ';' + 'region'+ ';' + 'language')

    for i in range(99280, 142392):
        
        #сбор данных
        
        URL = commonURL + str(i)
        html = read_html(URL)
        if html != '':
            csv(URL)
            file = 'article' + str(i)
            text = find_text(URL)
            if text != '':
                created = data_created(URL)
                if re.search(r'\d+\.\d+\.(\d+)', created):
                    year = re.search(r'\d+\.\d+\.(\d+)', created).group(1)
                else:
                    year = 'Unknown'
                    
                if re.search(r'\d+\.(\d+)\.\d+', created):
                    month = re.search(r'\d+\.(\d+)\.\d+', created).group(1)
                else:
                    month = 'Unknown'

                #создание папок    

                if os.path.exists(plain + '/' + year) != True:
                    os.mkdir(plain + '/' + year)
                if os.path.exists(plain + '/' + year + '/' + month) != True:
                    os.mkdir(plain + '/' + year + '/' + month)
                    
                if os.path.exists(m_xml + '/' + year) != True:
                    os.mkdir(m_xml + '/' + year)
                if os.path.exists(m_xml + '/' + year + '/' + month) != True:    
                    os.mkdir(m_xml + '/' + year + '/' + month)
             
                if os.path.exists(m_plain + '/' + year) != True:
                    os.mkdir(m_plain + '/' + year)
                if os.path.exists(m_plain + '/' + year + '/' + month) != True:
                    os.mkdir(m_plain + '/' + year + '/' + month)

                #создание txt-файлов

                author = data_author(URL)
                header = data_header(URL)
                created = data_created(URL)
                topic = data_topic(URL)

                with open ('newspaper/plain/' + year + '/' + month + '/' + file + '.txt', 'w', encoding = 'utf-8') as m:
                    m.write('@au ' + author + '\n' + '@ti ' + header + '\n' + '@da ' + created + '\n' + '@topic ' + topic + '\n' + '@url ' + URL + '\n')
                with open ('newspaper/plain/' + year + '/' + month + '/' + file + '.txt', 'a', encoding = 'utf-8') as l:
                    l.write(text)
                                
                mystem(year,month,file)
                            
                print(i)
                
        

#работа с mystem
                
def mystem(year, month, file):
    
    text_input = os.path.join('newspaper', 'plain', year, month, file + '.txt ')
    xml_output = os.path.join('newspaper', 'mystem-xml', year, month, file + '.xml')
    text_output = os.path.join('newspaper', 'mystem-plain', year, month, file + '.txt')

    os.system('mystem.exe ' + '-di ' + text_input + xml_output)
    os.system('mystem.exe ' + '-di ' + text_input + text_output)
        

folders()

