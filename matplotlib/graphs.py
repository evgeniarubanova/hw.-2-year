import re
import urllib.request  
import matplotlib.pyplot as plt


def read_html():
    user = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request('http://wiki.dothraki.org/Vocabulary', headers={'User-Agent':user})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def parts(html):
    reg_whole = re.compile('<ul><li><b>(\w*?)</b>(.*?)(<dd><i>(.*?)</i>(\w*?)</dd>)*</dl>', re.DOTALL)
    reg_parts = re.compile('<i>(.*?)</i>', re.DOTALL)
    d = {'nouns': '0', 'verbs': '0', 'adverbs': '0', 'adjectives': '0', 'determiners': '0', 'numerals': '0', 'conjunctions': '0', 'interjections': '0', 'pronouns': '0', 'proper nouns': '0', 'prepositions': '0'}
    words = re.findall(reg_whole, html)
    for i in words:
        for p in re.findall(reg_parts, i[1]):
            if p == 'na.' or p == 'ni.' or p == 'n.' or p == 'np.':
                d['nouns'] = str(int(d['nouns']) + 1)
            if p == 'v.' or p == 'vin.' or p == 'vtr.' or p == 'v. aux.':
                d['verbs'] = str(int(d['verbs']) + 1)
            if p == 'adv.':
                d['adverbs'] = str(int(d['adverbs']) + 1)
            if p == 'adj.':
                d['adjectives'] = str(int(d['adjectives']) + 1)
            if p == 'det.':
                d['determiners'] = str(int(d['determiners']) + 1)
            if p == 'num.':
                d['numerals'] = str(int(d['numerals']) + 1)
            if p == 'conj.':
                d['conjunctions'] = str(int(d['conjunctions']) + 1)
            if p == 'intj.':
                d['interjections'] = str(int(d['interjections']) +1)
            if p == 'pn.':
                d['pronouns'] = str(int(d['pronouns']) + 1)
            if p == 'prop. n.':
                d['proper nouns'] = str(int(d['proper nouns']) + 1)
            if p == 'prep.':
                d['prepositions'] = str(int(d['prepositions']) + 1)
    return d

def letters(html):
    reg_word = re.compile('<span id="(.*?)">', re.DOTALL)
    reg_letter = re.compile('<span class="mw-headline" id="(\w)">(.*?)<\/span><\/h3>(.*?)<h[23]>', re.DOTALL)
    l = {}
    for i in re.findall(reg_letter, html):
        l[i[0]]= '0'
        for w in re.findall(reg_word, i[2]):
            l[i[0]] = str(int(l[i[0]]) + 1)
    return l

def visual(html):
    d = parts(html)
    l = letters(html)
    
    p_list = []
    p_number = []
        
    for p in d:
        p_list.append(p) 
        p_number.append(int(d[p]))

    Xp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    Yp = p_number

    plt.xticks(Xp, p_list)
    plt.bar(Xp, Yp, color='green')
    plt.title('Количество слов каждой из частей речи')
    plt.show()

    l_list = []
    l_number = []
   
    for i in l:
        l_list.append(i) 
        l_number.append(int(l[i]))

    Xl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    Yl = l_number
    
    plt.xticks(Xl, l_list)
    plt.bar(Xl, Yl, color='yellow')
    plt.title('Количество слов для каждой буквы дотракийского языка')
    plt.show()

def main(html):
    visual(html)

if __name__ == '__main__':
    html = read_html()
    main(html)


