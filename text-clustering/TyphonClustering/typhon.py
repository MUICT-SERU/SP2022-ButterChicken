# from dataclasses import dataclass
from typing import Iterable
# Clustering modules
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
# unixcoder module
import torch
from unixcoder import UniXcoder
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
stopwords.append('‘')
stopwords.append('’')
# stopwords[10:20]
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('punkt')


class Typhon:
    def __init__(self) -> None:
        self.model = UniXcoder("microsoft/unixcoder-base")
        self.model.to(device)
        self.clustering_model = AgglomerativeClustering()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.porter_stemmer = PorterStemmer()
        self.wordnet_lemmatizer = WordNetLemmatizer()

        
    def fit(self, data):
        """Fit(Train) the AgglomerativeClustering model using the given matrix of vectorized data.
        """
        return self

    def predict(self, data):
        """Fit and predict the possible cluster from the given vectorzied Markdown data
        """
        return self

    def preprocess(self, list_mds, filter_result=False) -> list:
        """Preprocess the incoming array of raw Markdown into an array of list of preprocessed tokens.

        Parameters:
        filter_result: boolean -> Determine whether to drop items that is an empty value after preprocessing. If set to True, it is possible that the size of returned list may change.
        """
        def remove_hyperlink(text):
            text = re.sub(r'https?://\S+', "", text)
            text = " ".join(re.sub(r'https?://\S+', "", text).split())
            return text

        def remove_tags(text):
            return re.sub(r"<.*?>", " ", text)

        if filter_result:
            res_list = list(filter(None, res_list)) # Filter out the empty value

    def generate_embedding(self, markdown_list):
        print(type(markdown_list))
        tokens_ids = self.model.tokenize(markdown_list,max_length=512,mode="<encoder-only>",padding=True)
        source_ids = torch.tensor(tokens_ids).to(device)
        tokens_embeddings,content_embedding = self.model(source_ids)
        embeddings = content_embedding.detach().numpy().tolist()
        
        return embeddings
    
    def preprocess_to_csv(self, markdown_list):
        df = pd.DataFrame({'markdown_content': markdown_list})
        # Drop empty value from the input list
        df = df.dropna() 
        # Preprocess the text
        preprocessed_text = self.preprocess(df['markdown_content'].tolist())

        # Create a series from the preprocessed text
        preprocessed_markdown = pd.Series(preprocessed_text, index=df.index)

        # Get the indices of the non-null rows in the preprocessed_markdown series
        non_null_indices = preprocessed_markdown[preprocessed_markdown.notna()].index

        # Use the indices to select only the non-null rows in the preprocessed_markdown series
        df = df.loc[non_null_indices,:]
        preprocessed_markdown = preprocessed_markdown[non_null_indices]
        df['preprocessed_markdown'] = preprocessed_markdown

        # Remove rows where the preprocessed_markdown column is empty
        df = df[df['preprocessed_markdown'] != '']
        preprocessed_markdown = preprocessed_markdown[preprocessed_markdown != '']

        # Add the preprocessed_markdown series as a new column to the DataFrame
        df['preprocessed_markdown'] = preprocessed_markdown
        df.to_csv('test-preprocess-to-csv.csv')

        return None