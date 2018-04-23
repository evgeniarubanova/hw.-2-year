import urllib.request
import re
import json
import os
import matplotlib.pyplot as plt
import math
import numpy

#os.mkdir('posts')
#os.mkdir('comments')

group_id = '-76982440'
access_token = 'eeec364feeec364feeec364f64ee8e6dc0eeeeceeec364fb431a58d738c6d6d9ae6fcc4'
n = 500 #количество постов
k = 100
offsets = [str(i * 100) for i in range(n // 100)]
reg_clean = '[\.\?!"@№;%:?*_()-+=#$^&:;\'"><,/\|\\~`•]'

def get_posts():
    p = 0
    post_ids = []
    post_len = []
    for offset in offsets:
        req_posts = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=' + group_id + '&count=' + str(k) + '&offset=' + str(offset) + '&v=5.74&access_token=' + access_token)
        response_posts = urllib.request.urlopen(req_posts)
        result_posts = response_posts.read().decode('utf-8')
        data_posts = json.loads(result_posts)
        for i in range(k):
            p += 1
            text = data_posts['response']['items'][i]['text']
            if re.search(reg_clean, text):
                text = re.sub(reg_clean, "", text)
            words = text.split()
            if len(words) > 0:
                post_len.append(len(words)) 
                #with open ('posts/Пост №' + str(p) + '.txt', 'w', encoding = 'utf-8') as m:
                    #m.write(text)
            post_id = data_posts['response']['items'][i]['id']
            post_ids.append(post_id)
    return post_ids, post_len

         
def get_comments():
    post_ids, post_len = get_posts()
    s = 0
    av_comments_len = []
    for offset in offsets:
        for post_id in post_ids:
            s += 1
            if s <= 500:
                comments = []
                comment_len = []
                req_comments = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=' + group_id + '&post_id=' + str(post_id) + '&count=' + str(k) + '&offset=' + str(offset) + '&extended=1&v=5.74&access_token=' + access_token)
                response_comments = urllib.request.urlopen(req_comments)
                result_comments = response_comments.read().decode('utf-8')
                data_comments = json.loads(result_comments)
                total = data_comments['response']['count']
                for o in range(total):
                    if o < total:
                        try:
                            comment = data_comments['response']['items'][o]['text']
                            if re.search(reg_clean, comment):
                                comment = re.sub(reg_clean, "", comment)
                            words_com = comment.split()
                            if len(words_com) > 0:
                                comment_len.append(len(words_com))
                                comments.append(comment)
                        except:
                            break
                    else:
                        break
                    comments_string = '\n'.join(comments)
                    #with open ('comments/Комментарии к посту №' + str(s) + '.txt', 'w', encoding = 'utf-8') as m:
                        #m.write(comments_string)
                av_len_comm_of_each_post = math.ceil(numpy.mean(comment_len))
                av_comments_len.append(av_len_comm_of_each_post)
            else:
                break
    #av_comments_len = numpy.around(av_comments_len, decimals=0)
    return av_comments_len


def lens_graph():
    X = []
    Y = []
    post_ids, post_len = get_posts()
    av_comments_len = get_comments()
    for i in post_len:
        X.append(i)
    for k in av_comments_len:
        Y.append(k)
    plt.title('Соотношение длины поста со средней длиной его комментариев')
    plt.xlabel('Длина поста')
    plt.ylabel('Средняя длина комментариев')
    plt.bar(X, Y)
    plt.show()

get_posts()
get_comments()
lens_graph()

