#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# synonym file

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet

def retrieve_synsets(word):
    '''
    Retrive the list of wordnet synonyms for a given word, and it's definition.
    
    Args:
    word = text string
    
    Outputs:
    list of tuples (synonym name, synonym definition)
    '''
    
    syns = []
    for i in range(len(wordnet.synsets(word))):
                syns.append((wordnet.synsets(word)[i].name(),
                             wordnet.synsets(word)[i].definition()))
    return syns


def word_scorer(w1, w2 = None, with_similarity_score = False):
    '''
    Retrive the list of wordnet synonyms for a given word, and it's definition. Scores each against one specific synset.
    
    Args:
    w1 = word, text string, 'code'
    w2 = defined synset for similarity comparison, e.g. 'code.v.01'
    
    Outputs:
    list of tuples (synonym name, synonym definition, similarity score)
    '''

    syns = []
    w2 = wordnet.synset(w2)
    for i in range(len(wordnet.synsets(w1))):
        if with_similarity_score:
            if w2:
                syns.append((wordnet.synsets(w1)[i].name(),
                             wordnet.synsets(w1)[i].definition(),
                             w2.wup_similarity(wordnet.synsets(w1)[i])))
            else:
                break
                print('with_similarity_score set to True, but no w2 defined')
        else:
            syns.append((wordnet.synsets(w1)[i].name(),
                         wordnet.synsets(w1)[i].definition()))
    return syns


def sentence_cleaner(phrase):
    '''
    Removes stopwords, punctuation from text, and converts into a list of word tokens
    
    Args:
    phrase = text string
    
    Outputs:
    list of word tokens
    '''
    
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(phrase)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence


def topic_scorer(filtered_sentence, topic, sim_thresh = 0.6, return_hits = False):
    '''
    For each word in a sentence, retrieves the synonym set. For each synonym we measure the wup_similarity
    to the topic at hand. If similarity > sim_threshold, the topic is said to have been mentioned.
    
    Args:
    filtered_sentence = tokenized sentence, preferrably stripped of stopwords
    topic = Synset of the topic in question.
    sim_threshold = threshold for topic similarity (default = 0.6)
    
    Outputs:
    Integer count of the number of mentions of the topic in the filtered_sentence
    '''
    
    word_scores = []
    for w in range(len(filtered_sentence)):
        syns = wordnet.synsets(filtered_sentence[w])
        syns_sim = [topic.wup_similarity(syns[synonym]) for synonym in range(len(syns))]
        syns_sim = [sim if sim is not None else 0 for sim in syns_sim]
        try:
            syns_sim = np.max([1 if sim > sim_thresh else 0 for sim in syns_sim])
        except ValueError:
            syns_sim = 0
        word_scores.append(syns_sim)
    hits = [filtered_sentence[w] for w in range(len(filtered_sentence)) if word_scores[w] == 1]
        
    if return_hits:    
        return (np.sum(word_scores), hits)
    else:
        return np.sum(word_scores)


def phrase_scorer(phrase, topic_dictionary, sim_thresh=0.6, return_hits=False):
    '''
    Takes a passage of text and maps words in that text to topics that have been defined in a topic dictionary.
    
    Args:
    phrase = passage of text
    topic_dictionary = dictionary where key:value is reader-friendly topic name:assigned synonym in wordnet
    
    Outputs:
    sim_scores = dictionary where key:value is the reader-friendly topic name:number of synonyms present in the text
    '''
    
    sim_scores = {}
    for topic in list(topic_dictionary.keys()):
        topic_synset = wordnet.synset(topic_dictionary['{}'.format(topic)])
        sim_scores['{}'.format(topic)] = synonym_scorer(sentence_cleaner(phrase), topic_synset, sim_thresh, return_hits)
    return sim_scores

