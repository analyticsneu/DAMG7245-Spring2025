# RAG System Implementation Tutorials

This repository contains a series of Jupyter notebooks that demonstrate how to build and understand Retrieval Augmented Generation (RAG) systems from scratch, without relying on frameworks like LangChain or LlamaIndex.

## Notebooks Overview

### 1. Embedding Similarity Practical (01_embedding_similarity_practical.ipynb)
This notebook provides a practical guide to understanding text embeddings and similarity calculations for RAG systems. Topics covered:
- Introduction to embeddings and their importance
- Embedding models comparison (open-source and proprietary)
- Understanding similarity metrics (cosine, euclidean, dot product)
- Practical examples of embedding arithmetic
- Performance evaluations and comparisons

### 2. Chunking Strategies (02_chunking_strategies.ipynb)
A comprehensive exploration of different text chunking strategies for RAG systems:
- Basic chunking methods (character-based, token-based)
- Advanced strategies (recursive, semantic, cluster-based)
- Performance comparisons and benchmarks
- Decision matrix for choosing chunking strategies
- Best practices and recommendations

### 3. Basic RAG Tutorial (03_basic_rag_tutorial.ipynb)
A step-by-step guide to building a complete RAG system from scratch:
- Document collection and processing
- Implementation of chunking and embedding
- Vector storage using ChromaDB
- Retrieval system implementation
- Response generation with OpenAI
- Complete pipeline integration
- Testing and evaluation

## Purpose

These notebooks aim to provide a deep understanding of RAG systems by implementing core components from scratch. By avoiding high-level frameworks, you'll gain:
- Better understanding of RAG system internals
- More control over system behavior
- Ability to customize components for specific needs
- Deeper insights into optimization opportunities

## Important Note

The provided Create-LLama-Example folder serves as a reference implementation only. This project intentionally avoids using LlamaIndex, LangChain, or similar frameworks to provide a clearer understanding of RAG fundamentals. You are encouraged to implement components from scratch following the tutorials in the notebooks.


## Getting Started

1. Clone the repository
2. Install required dependencies
3. Follow the notebooks in order:
   - Start with embedding similarity concepts
   - Learn about chunking strategies
   - Build your own RAG system using the basic tutorial

## License

MIT License
