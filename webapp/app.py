# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:09:26 2020

@author: kvija
"""

import streamlit as st
import requests
import redis
import os
import time

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port)
redis_client.flushall()

def run_sent_freq(textlink):
    freq_link = "https://us-central1-vijaysai.cloudfunctions.net/sent_freq?link="+textlink
    freq = requests.get(freq_link)
    #cache on redis
    redis_client.rpush(textlink, freq.text)
    return freq.text

def run_plot_func(freq, textlink):
    plot_funclink = "https://us-central1-vijaysai.cloudfunctions.net/plot_hist?data="+freq+"&link="+textlink
    plot_link = requests.get(plot_funclink)
    #cache on redis
    redis_client.rpush(textlink, plot_link.text)
    return plot_link.text

def main():
    start_time = time.time()
    
    
    st.title('Sentence Length Frequency')
    #user inputs
    textlink = st.sidebar.text_input("Text Link")
    button_was_clicked = st.sidebar.button("Submit")
    if button_was_clicked:
        st.write("For text link: " + textlink)
        
        # if in cache
        if redis_client.exists(textlink):
            from_cache_data = redis_client.lrange(textlink, 0, -1)
            freq_dist = from_cache_data[0].decode('utf-8')
            plot_link = from_cache_data[1].decode('utf-8')
        
        # else run cloud functions
        else:
            freq_dist = run_sent_freq(textlink)
            plot_link = run_plot_func(freq_dist, textlink)
        
        #Display Frequency Output
        st.write("Frequency distribution of sentence lengths: (Format - {Sentence length: Number of occurrences})")
        st.write(freq_dist)
        
        #Display histogram image
        st.image(plot_link,width=650)
        st.write(f"Time taken in Seconds: {time.time()-start_time}")
        
if __name__ == '__main__':
    main()