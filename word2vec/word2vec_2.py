
# coding: utf-8

# In[3]:


import sys 
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)

model.init_sims(replace=True)


# In[30]:


def create_graph():
    words = ['ругать_VERB','обижать_VERB','бранить_VERB','кричать_VERB','наказывать_VERB','унижать_VERB','орать_VERB','стыдить_VERB','голосить_VERB','проклинать_VERB']  
    G = nx.Graph()
    G.add_nodes_from(words)
    try:
        for i in words:
            rest = words
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


# In[31]:


create_graph()

