# Agglomerative Clustering

The example code is taken from the Jupyter notebook lab from [notebook.community by donaghhorgan](https://notebook.community/donaghhorgan/COMP9033/labs/09b%20-%20Agglomerative%20clustering).

## General steps

- It clusters with bottom-up approach, an instance of document are considered as a single-cluster.
- Then, each cluster will compute its nearby cluster similarty and merge if they are similar.
- In the end, clusters are aggregated and the dendogram is formed.
