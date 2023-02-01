# All about UniXcoder that I am able to grasp from the paper

This documentation trys to note down the important detail from the UniXcoder paper that I think is quite important.

Table of content (What i want to tell)

1. Explain the terminology in the paper title
   1. Cross-modal
      1. code comment
      2. Abstract syntax tree (from code snippet)
   2. Unified
   3. Encoder-only
   4. Decoder-only
   5. Encoder-decoder
2. Important terminologies in the paper
   1. mask attention
   2. prefix adapter
   3. contrastive learning
   4. one-to-one mapping
      1. mapping the leaf node of AST(each token in the code) to each item in the sequence
3. Purpose of the model
   - improve efficiency over the encoder-decoder models
4. Pre-train for tasks
   3 type of lang modeling tasks
   1. masked language modeling
   2. unidirectional langauge modeling
   3. denoising objective
      and additional tasks for learning embedding that can represent semantics of code fragments
   4. multi-modal contrastive learning
      - use AST to make semantic of code fragment embedding more useful
   5. cross-modal generation
      - utilize code comment to kind of group the context of code among various of programming languages

## Terminologies Explained

1. Cross-modal\
   The term cross-modal generally means that the model leverages more than one type of data to produce embedding and pre-train code representation.

   <!-- Additionally, the [cross-modal deep learning](https://jina.ai/news/what-is-multimodal-deep-learning-and-what-are-the-applications/#:~:text=information%20from%20one%20modality%20is%20used%20to%20improve%20performance%20in%20another) also means that the model utilize information from one modality to improve performance in another modality. -->

   Which in this case, UniXcoder utilizes _code comment_ and _AST_ from the code snippet as the input to build an embedding representation from them.

2. Unified\
   The term unified in UniXcoder paper probably saying that the model combines multiple modalities (i.e. code comment, AST) into a single representation.

<!-- Below paragraphes are copied from ChatGPT -->
<!-- A unified model can process multiple types of inputs, such as text and images, in a coherent manner and learn a single representation that can be used for multiple tasks.

By combining multiple modalities into a single representation, the model can better understand the relationships between the modalities and make use of the complementary information provided by each modality to improve its overall performance. This is different from traditional models that treat each modality as separate inputs and learn a separate representation for each modality.

In the context of UniXcoder, the goal of the unified approach is to improve the model's ability to perform code-related understanding and generation tasks by considering not only code, but also code comments and abstract syntax trees. -->

3. Encoder-only\
   Let's clarify on the term **Encoder** as simply as possible. It means the process of generating embedding or vector representation from the input.

   Here, the term Encoder-only refers to the pre-trained model that only contains encoding functionality and cannot decode the encoded output by it own.

   To put into more practical sentences, it says that the pre-trained model can only generate the embedding representation from the input but does not have the capability to decode that embedding because it is not designed to have the decoder function.

   Therefore, another additional decoder for downstream tasks are required for encoder-only model. Which usually made from scratch and cannot benefit from the pre-training.

4. Decoder-only\
   Similar to encoder-only model. Decoder-only model can only produce the generated results from the downstream tasks, and unable to explicitly produce the the embedding representation for user-defined operation.

   The decoder model in this case, does not take embedding representation as an input to produce the generated result from the model, but similar to encoder-only model, it takes the regular input, process it, then produce the downstream task result.

   In the case of UniXcoder decoder-only mode, it takes the code snippet and code comment, then produce the human-understandable result instead of embedding representation as in encoder-only mode.

5. Encoder-Decoder\
   The Encoder-Decoder models have the capabilities to both generate embedding representation and decode the resulting embedding using its own function.

   **_Attention:_** There are more detail on the difference among encoder-only, decoder-only, and encoder-decoder. It is suggested that reader take a loog in [UniXcoder paper](https://arxiv.org/pdf/2203.03850.pdf), specifically in the section 2: Related Works part.

6. Mask Attention\
   Mask attention mechanism is a process in the Transformer model, (or just think of any NLP model would be fine) for preventing the model from attending to future tokens in the input sequence when generating representations for each token(From ChatGPT).

   Which the process takes place in each of the Tranformer layer as shown in the self/cross-attention pink circle in the picture below.

   <img src="https://vaclavkosar.com/images/transformer-full-model.png" alt="Tranformer Layers" width="400"/>
   <!-- ![](https://vaclavkosar.com/images/transformer-full-model.png) -->

   It was first introduced in the paper "Attention is all you need"" by Vaswani et al.(2017).

7. Prefix Adapter\
   <!-- The prefix in the UniXcoder refers to the prefix token used for putting at the beggining the of an input sequence. Just like any other NLP model where it require [CLS] token at the start, UniXcoder has its own prefixes to make the model has better control the access to context information, which can improve the performance of the model on various tasks. -->

   The Prefix Adapter in the UniXcoder refer to the mechanism for controlling the access to context information for each token in an input sequence. The prefix adapter acts as a gate that determines how much of the context information is used for each token.

   The purpose of this mechanism is to let the model adapt it encoding-decoding mode to satisfy the downstream tasks.

8. Contrastive Learning\
   Contrastive Learning is an unsupervised learning technique to make the positive samples stay close together and the negative samples to be far apart.

   This term is quite intuitive to think of, just think of the machine that does not learn only the positive samples but it also learn how to distinguish the negative samples.

9. One-to-one Mapping\
   The term one-to-one mapping in the UniXcoder paper refers to the tranformation of an AST into a vector sequence.

   Considering that the AST is a tree structure and therefore unable to process through the model. So the paper introduce an algorithm to turn each leaf node in the Abstract Syntax Tree into each token in the vector representation for processing in the model.
