# from dataclasses import dataclass
from typing import Iterable
from scipy.sparse._csr import csr_matrix

from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

class Typhon:
    def __init__(self) -> None:
        self.model = AgglomerativeClustering()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    
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

