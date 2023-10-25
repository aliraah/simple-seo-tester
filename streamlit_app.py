import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import streamlit as st

nltk.download('stopwords')
nltk.download('punkt')


st.title('Simple SEO Test')
url = st.text_input('Please Enter URL:')

def seo_test(url):
    
    bad = []
    good = []
    keywords = [] 
    score = float(0)

    html = requests.get(url)
    if html.status_code != 200:
        st.error('Error: Website cannot be reached!')
        return
    
    soup = BeautifulSoup(html.content, 'html.parser')
    
    #Grap the TITLE (text) of the page
    title = soup.find('title').text
    
    #If the TITLE exists, add it to the 'good' list
    if title:
        good.append(f'Title Found: {title}')
    else:
        bad.append('Title Not Found!')
    
    
    #Grap the META DESCRIPTION (content) of the page, handle the error if non existent
    try:
        meta_desc = soup.find('meta', {'name':'description'})['content']
        meta_desc_val = 1
    except:
        meta_desc_val = -1
    
    #If it exists, add to the good. Else, add to the bad
    if meta_desc_val > 0:
        good.append(f'Meta Description Found: {meta_desc}')
    else:
        bad.append('Meta Description Not Found!')
    
    
    headings = ['h1', 'h2', 'h3']
    existing_tags = []
    #Find all the H TAGS(1-3) and lists them in 'existing_tags', also appends their value in 'good'
    for h in soup.find_all(headings):
        good.append(f'{h.name} --> {h.text.strip()}')
        existing_tags.append(h.name)
        score+=0.25
    
    if 'h1' not in existing_tags:
        bad.append('No H1 Tags Found!')
    elif 'h2' not in existing_tags:
        bad.append('No H2 Tags Found!')
    elif 'h3' not in existing_tags:
        bad.append('No H3 Tags Found!')
    
    #Grap all IMAGES(tags) of the page, find the ones without alts, grab the 'src' attritbute and append to bad list 
    for i in soup.find_all('img', alt=''):
        #noalt_img = soup.find('img')['src']
        bad.append(f'Image With No Alt Found:{i}')

    #Keywords
    #Grap only the BODY tag to analyze the text
    body = soup.find('body').text

    #Grap all the words/tokens on the page, turn them to lowercase and store the in the 'words' list
    words = [i.lower() for i in word_tokenize(body)]


    #Use ngrams library and our words list to extract bi_grams on the page (use 3 for tri_grams and so on)
    bi_grams = ngrams(words, 2)
    freq_bigrams = nltk.FreqDist(bi_grams)
    common_bigrams = freq_bigrams.most_common(10)

    tri_grams = ngrams(words, 3)
    freq_trigrams = nltk.FreqDist(tri_grams)
    common_trigrams = freq_trigrams.most_common(10)

    #Get all the English 'stopwrods' we have downloaded from nltk
    stop_words = nltk.corpus.stopwords.words('english')

    #Check our 'words' list, grab the ones that are not 'stop_words', and are not a character or a number (i.isalpha()) and add to 'useful_words'
    useful_words = []
    for i in words:
        if i not in stop_words and i.isalpha():
            useful_words.append(i)

    #Check the frequency distribution of the useful_words
    freq = nltk.FreqDist(useful_words)
    keywords = freq.most_common(10)

    #Output:

    x = len(good)
    y = len(bad)
    z = x - y

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Keywords', 'BiGrams', 'TriGrams', 'Positive', 'Negative', 'Score'])
    with tab1:
    	#st.write(keywords)
    	for i in keywords:
    		#st.text(i)
    		st.info(i)
    with tab2:
    	#st.write(common_bigrams)
    	for i in common_bigrams:
    		#st.text(i)
    		st.info(i)
    with tab3:
    	for i in common_trigrams:
    		#st.text(i)
    		st.info(i)
    with tab4:
    	#st.write(good)
    	for i in good:
    		st.success(i)
    with tab5:
    	#st.write(bad)
    	for i in bad:
    		st.error(i)
    with tab6:
    	st.write('Score:', z)


    #print('Score:')
    #print(z)

if url:
	seo_test(url)
