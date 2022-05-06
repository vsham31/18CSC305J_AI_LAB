!pip install -q wordcloud

import wordcloud

 

import nltk

nltk.download('stopwords')

nltk.download('wordnet')

nltk.download('punkt')

nltk.download('averaged_perceptron_tagger') 

 

import pandas as pd

import matplotlib.pyplot as plt

import io

import unicodedata

import numpy as np

import re

import string

# Constants

# POS (Parts Of Speech) for: nouns, adjectives, verbs and adverbs

DI_POS_TYPES = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'} 

POS_TYPES = list(DI_POS_TYPES.keys())

 

# Constraints on tokens

MIN_STR_LEN = 3

RE_VALID = '[a-zA-Z]'

# Upload from google drive

from google.colab import files

uploaded = files.upload()

print("len(uploaded.keys():", len(uploaded.keys()))

 

for fn in uploaded.keys():

  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))

 

# Get list of quotes

df_quotes = pd.read_csv(io.StringIO(uploaded['quotes.txt'].decode('utf-8')), sep='\t')

  

# Display

print("df_quotes:")

print(df_quotes.head().to_string())

print(df_quotes.describe())

 

# Convert quotes to list

li_quotes = df_quotes['Quote'].tolist()

print()

print("len(li_quotes):", len(li_quotes)

# Get stopwords, stemmer and lemmatizer

stopwords = nltk.corpus.stopwords.words('english')

stemmer = nltk.stem.PorterStemmer()

lemmatizer = nltk.stem.WordNetLemmatizer()

 

# Remove accents function

def remove_accents(data):

    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters or x == " ")

 

# Process all quotes

li_tokens = []

li_token_lists = []

li_lem_strings = []

 

for i,text in enumerate(li_quotes):

    # Tokenize by sentence, then by lowercase word

    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

 

    # Process all tokens per quote

    li_tokens_quote = []

    li_tokens_quote_lem = []

    for token in tokens:

        # Remove accents

        t = remove_accents(token)

 

        # Remove punctuation

        t = str(t).translate(string.punctuation)

        li_tokens_quote.append(t)

        

        # Add token that represents "no lemmatization match"

        li_tokens_quote_lem.append("-") # this token will be removed if a lemmatization match is found below

 

        # Process each token

        if t not in stopwords:

            if re.search(RE_VALID, t):

                if len(t) >= MIN_STR_LEN:

                    # Note that the POS (Part Of Speech) is necessary as input to the lemmatizer 

                    # (otherwise it assumes the word is a noun)

                    pos = nltk.pos_tag([t])[0][1][:2]

                    pos2 = 'n'  # set default to noun

                    if pos in DI_POS_TYPES:

                      pos2 = DI_POS_TYPES[pos]

                    

                    stem = stemmer.stem(t)

                    lem = lemmatizer.lemmatize(t, pos=pos2)  # lemmatize with the correct POS

                    

                    if pos in POS_TYPES:

                        li_tokens.append((t, stem, lem, pos))

 

                        # Remove the "-" token and append the lemmatization match

                        li_tokens_quote_lem = li_tokens_quote_lem[:-1] 

                        li_tokens_quote_lem.append(lem)

 

    # Build list of token lists from lemmatized tokens

    li_token_lists.append(li_tokens_quote)

    

    # Build list of strings from lemmatized tokens

    str_li_tokens_quote_lem = ' '.join(li_tokens_quote_lem)

    li_lem_strings.append(str_li_tokens_quote_lem)

    

# Build resulting dataframes from lists

df_token_lists = pd.DataFrame(li_token_lists)

 

print("df_token_lists.head(5):")

print(df_token_lists.head(5).to_string())

 

# Replace None with empty string

for c in df_token_lists:

    if str(df_token_lists[c].dtype) in ('object', 'string_', 'unicode_'):

        df_token_lists[c].fillna(value='', inplace=True)

 

df_lem_strings = pd.DataFrame(li_lem_strings, columns=['lem quote'])

 

print()

print("")

print("df_lem_strings.head():")

print(df_lem_strings.head().to_string())

# Add counts

print("Group by lemmatized words, add count and sort:")

df_all_words = pd.DataFrame(li_tokens, columns=['token', 'stem', 'lem', 'pos'])

df_all_words['counts'] = df_all_words.groupby(['lem'])['lem'].transform('count')

df_all_words = df_all_words.sort_values(by=['counts', 'lem'], ascending=[False, True]).reset_index()

 

print("Get just the first row in each lemmatized group")

df_words = df_all_words.groupby('lem').first().sort_values(by='counts', ascending=False).reset_index()

print("df_words.head(10):")

print(df_words.head(10))

df_words = df_words[['lem', 'pos', 'counts']].head(200)

for v in POS_TYPES:

    df_pos = df_words[df_words['pos'] == v]

    print()

    print("POS_TYPE:", v)

    print(df_pos.head(10).to_string())

li_token_lists_flat = [y for x in li_token_lists for y in x]  # flatten the list of token lists to a single list

print("li_token_lists_flat[:10]:", li_token_lists_flat[:10])

 

di_freq = nltk.FreqDist(li_token_lists_flat)

del di_freq['']

li_freq_sorted = sorted(di_freq.items(), key=lambda x: x[1], reverse=True)  # sorted list

print(li_freq_sorted)

    

di_freq.plot(30, cumulative=False)

li_lem_words = df_all_words['lem'].tolist()

di_freq2 = nltk.FreqDist(li_lem_words)

li_freq_sorted2 = sorted(di_freq2.items(), key=lambda x: x[1], reverse=True)  # sorted list

print(li_freq_sorted2)

    

di_freq2.plot(30, cumulative=False)

