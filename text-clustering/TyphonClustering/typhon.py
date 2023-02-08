# from dataclasses import dataclass
from typing import Iterable
# Clustering modules
from scipy.sparse._csr import csr_matrix
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
# Preprocess modules
import pandas as pd
import string
import re
## import NLP lib and its stopwords module
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
# stopwords[10:20]
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('punkt')


class Typhon:
    def __init__(self) -> None:
        self.model = AgglomerativeClustering()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.porter_stemmer = PorterStemmer()
        self.wordnet_lemmatizer = WordNetLemmatizer()
    
    # def vectorizMarkdown(self, markdown: Iterable, method="tfidf") -> csr_matrix:
    #     """Return the collection of vectorized Markdown text using specified vectorization method.

    #     Default vectorization is Tf-Idf vectorizer. Another vectorizer technique is using CodeBERT.

    #     Parameters
    #     ----------
    #     markdown : Iterable
    #         The collection of markdown to be vectorized.
    #         If raw text is given, it will automatically be converted to list.

    #     method : {"tfidf", "codebert"}, default='tfidf'
    #         The approach to vectorize the text. 

    #     Return
    #     ----------
    #     Sparse matrix of (n_samples, n_features)
    #     """
    #     markdown_vectorized = self.tfidf_vectorizer.fit_transform(markdown)
    #     return self
        
    def fit(self, data: csr_matrix):
        """Fit(Train) the AgglomerativeClustering model using the given matrix of vectorized data.
        """
        return self

    def predict(self, data: csr_matrix):
        """Fit and predict the possible cluster from the given vectorzied Markdown data
        """
        return self

    def preprocess(self, list_mds: list) -> list:
        """Preprocess the incoming array of raw Markdown into an array of list of preprocessed tokens.
        """
        # if not (isinstance(list_mds, list)):
        #     raise TypeError("param must be of type <List>")
            
        def remove_hyperlink(text):
            text = re.sub(r'https?://\S+', "", text)
            text = " ".join(re.sub(r'https?://\S+', "", text).split())
            return text

        def remove_tags(text):
            return re.sub(r"<.*?>", " ", text)

        def tokenization(text):
            text = text.lower()
            text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text).strip() # replace punctuation with ' '(space)
            text = " ".join(text.split()) # remove the excess spaces and newlines
            return nltk.word_tokenize(text)

        def remove_stopwords(tokens):
            return [token for token in tokens if token not in stopwords]
            
        def stemming(tokens):
            return [self.porter_stemmer.stem(token) for token in tokens]

        def lemmatizer(tokens):
            return [self.wordnet_lemmatizer.lemmatize(token) for token in tokens]

        res_list = []
        for md in list_mds:
            # print(md)
            staging_md = remove_hyperlink(md)
            staging_md = remove_tags(staging_md)
            staging_md = tokenization(staging_md)
            staging_md = remove_stopwords(staging_md)
            staging_md = stemming(staging_md)
            staging_md = lemmatizer(staging_md)
            res_list.append(staging_md)
        # print(res_list)
        # print('morning')
        return res_list