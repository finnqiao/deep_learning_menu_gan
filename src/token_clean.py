import pandas as pd
import numpy as np
import nltk
import missingno as msno
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

df = pd.read_csv('../data/external/menupages.csv')

msno.matrix(df)

df[df['menu_descriptions'].isna()]

test_df = df.loc[[19,36,37,48],]

test_df

tokenizer = RegexpTokenizer(r'\w+')

for row in test_df.itertuples():
    print(row[2])

for row in test_df.itertuples():
    tokens = tokenizer.tokenize(row[2])
    words = [word for word in tokens if word.isalpha()]
    print(words)

from nltk.tokenize import RegexpTokenizer

def remove_punc(df, index):
    tokenizer = RegexpTokenizer(r'\w+')
    return_series = []
    for row in df.itertuples():
        tokens = tokenizer.tokenize(row[index])
        words = [word for word in tokens if word.isalpha()]
        words = (' ').join(words)
        return_series.append(words)
    print(len(return_series))
    return pd.Series(return_series)


remove_punc(test_df, 2)




#
