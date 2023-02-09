# Typhon: Code Recommendation Tool For Jupyter Notebook

## Description

This repository contains the source code of Typhon library, which is a code recommendation tool that utilize the hierarchical clustering model to organize the data and find the similarity with couple of approches, namely, using BM25 in Elasticsearch on text and utilize CodeBERT to assist in vectorization for further similarity finding.

This project is a senior project of 4th year student at the Faculty of Information and Communication Technology, Mahidol University.

## Usage

Before using Typhon, it is best to install dependencies listed in the `requirements.txt` file.

<!-- Then, import the file as a regular library in the working file. -->

<!-- ### Installing -->

<!-- ### Folder Structure -->

## Methods

### fit **(Work in progress)**

Fit method will fit(train) the clustering model of the module.

### predict **(Work in progress)**

Predict method will return the prediction result of the clustering model from the input.

### preprocess

Preprocess method will take an array of raw Markdown, do NLP preprocess, and return the array of processed Markdown items.

**Parameters:**

- _(require)_ list_mds : `List<str>`
- filter_result: `boolean` = True(Default) -> Determine whether to drop items that is an empty value after preprocessing.\
  If set to True, it is possible that the size of returned list may change.

**Return**

- List<str> of processed Markdown

### preprocess_to_csv

This method did the same as `preprocess()` method, it takes the list of raw Markdown and result in processed Markdown. Only that this method does not return the array of processed Markdown, it create a CSV file of the result.

**Parameters:**

- _(require)_ markdown_list : `List<str>`

**Return**

- Create CSV file of processed Markdown

**Todo**

1. Should take the filename as an argument.

### generate_embedding

This method takes the list of preprocessed Markdown, then generate the embedding representation of the provided input.

**Parameters:**

- _(require)_ markdown_list : `List<str>`

**Return**

- List< of List<float> > of Markdown embedding representation
