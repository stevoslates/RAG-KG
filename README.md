# Knowledge Graphs for RAG 
Investigating the potential of Knowledge Graphs as a dynamic graph database for RAG applications\
**Key Idea:** be able to dynamically update the graph on updates and use them in real time.

Using LangChain to help construct Knowledge Graphs (KGs) with Neo4j Aura DB. Program allows creation of KGs from unstructured text, using Wikipedia pages to begin. Additionally, using LangChain's Cypher Chain to turn natural language queries into Cypher (Query Language for KGs) queries and output results. Program also allows for Cypher queries to be written directly.

Next Steps: Use related corpus of documents and create one KG, ensuring that we use the current schema each time a new document is added to pass to the LLM, to prevent duplicate entites being created e.g "John Smith" and "John S.".

