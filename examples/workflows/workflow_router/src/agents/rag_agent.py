"""
RAG Agent for document retrieval and question answering using Qdrant vector database.
"""
from mcp_agent.agents.agent import Agent


def create_rag_agent() -> Agent:
    """
    Creates a RAG agent specialized for document retrieval and question answering.
    
    Uses Qdrant vector database server for semantic search and retrieval.
    Ideal for queries about stored documents, knowledge bases, and information retrieval.
    
    Returns:
        Agent: Configured RAG agent with Qdrant server access
    """
    return Agent(
        name="rag_agent",
        instruction="""You are a specialized RAG (Retrieval-Augmented Generation) agent with access to a Qdrant vector database.
        
        Your capabilities include:
        - Semantic document search and retrieval
        - Question answering based on stored documents
        - Finding relevant information from knowledge bases
        - Vector similarity searches
        
        When processing queries:
        1. Use vector search to find relevant documents
        2. Analyze retrieved content for accuracy
        3. Provide comprehensive answers based on the retrieved information
        4. Cite sources when possible
        
        You excel at:
        - "Find documents about..."
        - "What does the documentation say about..."
        - "Search for information on..."
        - "Retrieve relevant content for..."
        """,
        server_names=["qdrant", "filesystem"]
    )


# Keywords that indicate RAG agent should handle the request
RAG_KEYWORDS = [
    "search", "find", "retrieve", "document", "documentation", "knowledge",
    "information", "research", "lookup", "query", "database", "content",
    "reference", "source", "article", "paper", "manual", "guide"
]

# Example queries that RAG agent handles well
RAG_EXAMPLES = [
    "Find documents about machine learning algorithms",
    "What does the API documentation say about authentication?",
    "Search for information on deployment best practices",
    "Retrieve content related to security guidelines",
    "Look up documentation for the payment API"
]