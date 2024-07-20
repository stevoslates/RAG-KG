### FOR CONSTRUCTING GRAPH ###
import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_community.graphs import Neo4jGraph
from loadData import loadWikiData, loadText, loadCSV, loadPdf
from langchain_experimental.graph_transformers import LLMGraphTransformer


#env vars
os.environ["OPENAI_API_KEY"]
os.environ["NEO4J_USERNAME"]
os.environ["NEO4J_URI"]
os.environ["NEO4J_PASSWORD"]

#Initlialise graph
graph = Neo4jGraph()

#Initialise LLM
llm = ChatOpenAI(temperature=0, 
model_name="gpt-4-turbo")

llm_transformer = LLMGraphTransformer(
    llm=llm
    #allowed_nodes=["INSERT LIST OF ALLOWED NODES HERE"],
    #allowed_relationships=["INSERT LIST OF ALLOWED RELATIONSHIPS HERE"],
    #node_properties=["INSERT LIST OF NODE PROPERTIES HERE"],
)

#Create graph documents
#Could be wiki data, text, csv, pdf (Wiki requires a page name and number of sentences)
text = loadWikiData("Barack Obama", 10)

#must be sotred as a langchain Document()
documents = [Document(page_content=text)]

graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")

# ONLY USE THIS WHEN YOU WANT TO ACTUALLY ADD THE EXTRACTED ENTITIES & RELATIONSHIPS TO AURADB GRAPH
graph.add_graph_documents(
  graph_documents, 
  baseEntityLabel=True, 
  include_source=True
)

