import nltk
import string
from heapq import nlargest
from nltk.corpus import stopwords
import streamlit as st

st.title('TEXT SUMMARIZER')

def preprocess_text(text):
    nopuch = [i for i in text if i not in string.punctuation]
    nopuch = "".join(nopuch)
    processed_text = [i for i in nopuch.split() if i.lower() not in stopwords.words('english')]
    return processed_text

def summary_generation(text):
    if text.count(". ") > 20:
        length = int(round(text.count(". ")/10, 0))
    else:
        length = 1

    proc_text = preprocess_text(text)

    word_freq = {}
    for i in proc_text:
        if i not in word_freq:
            word_freq[i] = 1
        else:
            word_freq[i] += 1

    max_freq = max(word_freq.values())
    for i in word_freq.keys():
        word_freq[i] = (word_freq[i]/max_freq)

    sent_list = nltk.sent_tokenize(text)

    sent_score = {}
    for sent in sent_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq:
                if sent not in sent_score:
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]

    summary_sent = nlargest(length, sent_score, key=sent_score.get)
    summary = " ".join(summary_sent)

    return summary

text = st.text_area('Enter the text to summarize')
submit_button = st.button('Submit')
if submit_button:
    summ = summary_generation(text)
    st.write(summ)



