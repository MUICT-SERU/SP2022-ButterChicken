# **Cross-Encoder approach for Markdown-to-code recommendation**

This repository dedicates to the cross-encoder study for assist in finding an approach to apply the cross-encoding model for our markdown-to-code recommendation.

## **Encoder Background Detail**

This section will try to provide a background knowledge about the cross-encoder and bi-encoder. I will try to explain as intuitive as possible for us who do not possess the technical and deep knowledge in the domain.

Also to note, this repository focuses on the [Sentence Transformer](https://www.sbert.net/index.html) BERT model.

### **Cross-encoder VS Bi-encoder**

![Bi_vs_Cross-Encoder.png](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/3569efce-f306-47e4-83cb-2a458dd2f925/Bi_vs_Cross-Encoder.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230131%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230131T082039Z&X-Amz-Expires=86400&X-Amz-Signature=b716be9817d364bf920c8d03081436f6ee1c4d12242271f66f52accf9b9b6603&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Bi_vs_Cross-Encoder.png%22&x-id=GetObject)

First, it is important to understand the steps in Bi-encoder and Cross-encoder. Although two of them try to find the similarity between 2 entities of vectors, there are big difference in the methodology.

**Bi-encoder** is usually composed of two of the same models with the same configuration and weight, and each text input will be encoded independently. Then, the model produces sentence embedding(vector) for each input sentence.

For example input sentences _A_ and _B_ → output sentence embedding _u_ and _v_

**Cross-encoder**, on the contrary, takes in the same input but produces a different result. But most important, it takes the sentences input simultaneously into the Transformer model and produces the value between 0 and 1, indicating the similarity between the two input sentences.

[Cross-Encoders - Sentence-Transformers documentation](https://www.sbert.net/examples/applications/cross-encoder/README.html#bi-encoder-vs-cross-encoder)

Reference to the above information

If the writing above does not make a clear understand. I suggest to read from the source instead

1. [Cross-Encoders - Sentence-Transformers documentation](https://www.sbert.net/examples/applications/cross-encoder/README.html#bi-encoder-vs-cross-encoder)\
   **_Source_**

2. [Using Cross-Encoders as reranker in multistage vector search | Weaviate - vector search engine](https://weaviate.io/blog/using-cross-encoders-as-reranker-in-multistage-vector-search)

3. [Sentence-CROBI: A Simple Cross-Bi-Encoder-Based Neural Network Architecture for Paraphrase Identification](https://www.mdpi.com/2227-7390/10/19/3578/pdf)\
   Look at Related work, around the top part is about **cross-encoder**, and the bottom of Related work is about **bi-encoder**

4. [Squeezing Water from a Stone: A Bag of Tricks for Further Improving Cross-Encoder Effectiveness for Reranking](https://cs.uwaterloo.ca/~jimmylin/publications/Pradeep_etal_ECIR2022.pdf)\
   Look at related work
