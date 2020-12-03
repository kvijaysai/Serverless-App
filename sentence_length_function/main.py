
import requests
from nltk import tokenize
import nltk
from flask import escape


def sent_freq(request):
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'link' in request_json:
        link = request_json['link']
    elif request_args and 'link' in request_args:
        link = request_args['link']
    else:
        link = 'L'
    
    nltk.download('punkt')
    f = requests.get(link)
    sentences = tokenize.sent_tokenize(f.text)
    len_sents = [len(tokenize.word_tokenize(i)) for i in sentences]
    distribution ={i:len_sents.count(i) for i in set(len_sents)}
    
    return escape(distribution)