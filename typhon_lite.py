import torch
from unixcoder import UniXcoder
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import re
import string
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
stopwords = nltk.corpus.stopwords.words('english')
stopwords.append('‘')
stopwords.append('’')

class Typhon:
    def __init__(self) -> None:
        self.model = UniXcoder("microsoft/unixcoder-base")
        self.model.to(device)
        # self.clustering_model = AgglomerativeClustering(n_clusters=8, linkage='ward')
        # self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.porter_stemmer = PorterStemmer()
        self.wordnet_lemmatizer = WordNetLemmatizer()

    def preprocess(self, list_mds, filter_result=True) -> list:
        """Preprocess the incoming array of raw Markdown into an array of list of preprocessed tokens.

        Parameters:
            - (require) list_mds : List<str>
            - filter_result: boolean = True(Default) -> Determine whether to drop items that is an empty value after preprocessing. If set to True, it is possible that the size of returned list may change.
        """
        def remove_hyperlink(text):
            text = re.sub(r'https?://\S+', "", text)
            text = " ".join(re.sub(r'https?://\S+', "", text).split())
            return text
        
        res_list = []
        for md in list_mds:
            processing_text = str(md)
            processing_text = processing_text.lower()
            processing_text = re.sub(r'\\n', r'', processing_text) # Remove \n from the text, it is not '\n' it is actually '\\n', gave me headache.
            processing_text = re.sub(f"[{re.escape(string.punctuation)}]", " ", processing_text).strip() # Remove punctuations
            processing_text = " ".join(processing_text.split()) # Remove excess spaces
            processing_text = remove_hyperlink(processing_text) # Remove hyperlink in text
            processing_text = re.sub(r"<.*?>", " ", processing_text) # Remove tags (<...>) in text
            processing_text = re.sub(r'[^a-zA-Z0-9\s]', "", processing_text) # Remove non-alphabetical letters

            processing_tokens = nltk.word_tokenize(processing_text)
            processing_tokens = [token for token in processing_tokens if token not in stopwords]
            processing_tokens = [self.porter_stemmer.stem(token) for token in processing_tokens]
            processing_tokens = [self.wordnet_lemmatizer.lemmatize(token) for token in processing_tokens]
            processed_text = " ".join(processing_tokens)
            # print(processed_text)
            res_list.append(processed_text)
        if filter_result:
            res_list = list(filter(None, res_list)) # Filter out the empty value

        return res_list
    
    def generate_embedding(self, markdown_list):
        # print(type(markdown_list))
        tokens_ids = self.model.tokenize(markdown_list,max_length=512,mode="<encoder-only>",padding=True)
        source_ids = torch.tensor(tokens_ids).to(device)
        tokens_embeddings,content_embedding = self.model(source_ids)
        embeddings = content_embedding.detach().numpy().tolist()
        
        return embeddings