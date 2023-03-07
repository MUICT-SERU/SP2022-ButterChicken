import torch
from unixcoder import UniXcoder
import numpy
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Typhon:
    def __init__(self):
        self.model = UniXcoder("microsoft/unixcoder-base")
        self.model.to(device)
        self.meta = {
                "name": "nah",
                "lang": "en"
                }
        
    def embedding(self, markdown):
        tokens_ids = self.model.tokenize(markdown, max_length=512, mode="<encoder-only>", padding=True)
        source_ids = torch.tensor(tokens_ids).to(device)
        tokens_embeddings, content_embedding = self.model(source_ids)
        embedding = content_embedding.detach().numpy().tolist()
        return embedding[0]

