import os
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_community.graphs import Neo4jGraph
from loadData import loadWikiData, loadText, loadCSV, loadPdf
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.chains import GraphCypherQAChain

# Set environment variables
#os.environ["OPENAI_API_KEY"]
#os.environ["NEO4J_USERNAME"]
#os.environ["NEO4J_URI"]
#os.environ["NEO4J_PASSWORD"]

def initialize_graph_and_llm():
    """Initializes the Neo4j graph and LLM."""
    graph = Neo4jGraph()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    llm_transformer = LLMGraphTransformer(
        llm=llm
        # allowed_nodes=["INSERT LIST OF ALLOWED NODES HERE"],
        # allowed_relationships=["INSERT LIST OF ALLOWED RELATIONSHIPS HERE"],
        # node_properties=["INSERT LIST OF NODE PROPERTIES HERE"],
    )
    return graph, llm, llm_transformer

def construct_graph(graph, llm_transformer, text_data):
    """Constructs the graph from provided text data using LLM."""
    documents = [Document(page_content=text_data)]
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    print(f"Nodes: {graph_documents[0].nodes}")
    print(f"Relationships: {graph_documents[0].relationships}")

    # Add extracted entities and relationships to the Neo4j graph
    graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)

def query_graph_with_llm(graph, llm, query):
    """Queries the graph using the provided LLM."""
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True) #can add the schema to use and the allowed nodes and relationships
    response = chain.invoke({"query": query})
    return response

def query_graph_with_cypher(graph, query):
    """Queries the graph using the provided Cypher query."""
    '''
    Cypher to return all entity names (assuming stored in 'id' property): 
        MATCH (n)
        WHERE n.id IS NOT NULL
        RETURN n.id AS entityId

    Will use this to restrict new entities being created to try and match to exisiting entities as much as LLM can.

    Can use graph.schema to get relationships, and pass this as well.
    '''
    response = graph.query(query)
    return response

# Example Usage
if __name__ == "__main__":
    
    # Initialize graph and LLM
    graph, llm, llm_transformer = initialize_graph_and_llm()
    
    # Load and construct graph from text data
    text_data = loadWikiData("Barack Obama", 10)

    # Example of text data for direct input
    #text_data = "Barack Hussein Obama II has a brother called Steven Slater"

    construct_graph(graph, llm_transformer, text_data)
    
    # Query the graph
    query = "Who is Barack Obama's sibling?"
    response = query_graph(graph, llm, query)
    print(response)
    

    #Command to get Graph Schema
    print(graph.schema)

    #Command to get all entity names
    query = "MATCH (n) WHERE n.id IS NOT NULL RETURN n.id AS entityId"
    response = query_graph_with_cypher(graph, query)
    print(response)