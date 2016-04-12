# Document-Parser-and-Indexer
This is a sample document parser and indexer built in Python to do searching on the documents corpus. 

1. EditDistance.py : Initial Code is a simple Edit distance Code. Currently this is not used by the Indexer, however it may be an alternative to jaccard coefficient used for spell corrections, as per the requirements.
2. Downloading_books.py: Downloading sample documents from archive.org. This is a python code to download documents into your corpus. One can add more links to the corpus and update code accordingly.
3. indexer+queryEngine.py: Here we build a Term-document Inverted Index, to be used for searching the corpus. The indexer also includes code to build Bigram index. Bigram Indexer is used to here to correct spell errors using Jaccard coefficient.
