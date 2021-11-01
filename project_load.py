# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:21:17 2021

@author: Ziyuan
"""
#project

import bert as br
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
nlp = spacy.load("en_core_web_sm")


with open(r"C:\Users\Ziyuan\OneDrive\桌面\a1.txt","r", encoding="utf-8")as f:
    text=f.read()

text_sentences = nlp(text)

whole_text=[]
for sentence in text_sentences.sents:
    sentence_tokens=[]
    for token in sentence:
        if(token.is_punct or token.is_space):
            continue
        else:         
        
            if nlp.vocab[token.lemma_].is_stop == False:
                sentence_tokens.append(token.lemma_)
                print(token.lemma_)
    whole_text.append(sentence_tokens)
         
    
        
