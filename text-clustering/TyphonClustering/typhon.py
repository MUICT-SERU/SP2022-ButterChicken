# from dataclasses import dataclass
from typing import Iterable

from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

class Typhon:
    def __init__(self) -> None:
        self.model = AgglomerativeClustering()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    
    def vectorizMarkdown(self, markdown: Iterable, method="tfidf"):
        """Return the collection of densed vectorized Markdown text using specified vectorization method.

        Default vectorization is Tf-Idf vectorizer. Another vectorizer technique is using CodeBERT.

        Parameters
        ----------
        markdown : Iterable
            The collection of markdown to be vectorized.
            If raw text is given, it will automatically be converted to list.

        method : {"tfidf", "codebert"}, default='tfidf'
            The approach to vectorize the text. 
        """
        markdown_vectorized = self.tfidf_vectorizer.fit_transform(markdown)
        return "sda"
