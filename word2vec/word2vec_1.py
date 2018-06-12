
# coding: utf-8

# In[1]:


import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)

model.init_sims(replace=True)


# In[2]:


def synonyms():
    word = input('Введите слово в формате глагол_VERB или существительное_NOUN и т.п.: ')
    d = {}
    items = []
    reg_i = re.compile("_(.*)'", re.DOTALL)
    reg_word = re.compile("_(.*)", re.DOTALL)
    s = 0
    if word in model:
        try:
            for i in model.most_similar(positive=[word], topn = 40):
                if re.search(reg_i, str(i)):
                    pos_i = re.search(reg_i, str(i)).group(1)
                    pos_word = re.search(reg_word, word).group(1)
                    if pos_i == pos_word:
                        s += 1
                        if s<11:
                            items.append(i[0])
                            d[((i[0]).split('_')[0])] = i[1]
        except KeyError:
            pass
    else:
        print("'" + word + "'" + ' ' + 'отсутствует в модели. Введите другое слово.')
    return d, items


# In[40]:


def create_graph():
    G = nx.Graph()
    d, items = synonyms()
    G.add_nodes_from(items)
    try:
        for i in items:
            rest = items
            for r in rest:
                if model.similarity(i, r)>0.5 and i != r:
                    G.add_edge(i, r)
    except KeyError:
        pass
    
    
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='pink', node_size=30) 
    nx.draw_networkx_edges(G, pos, edge_color='purple') 
    plt.axis('off')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
    plt.show() 
    
    deg = nx.degree_centrality(G)
    print('Топ 3 самых центральных слов графа: ')
    for nodeid in sorted(deg, key=deg.get, reverse=True)[:3]:
        print('\t', nodeid)
    print('Радиус графа = ', nx.radius(G))
    print('Коэффициент кластеризации = ', nx.average_clustering(G))


# In[41]:


create_graph()

