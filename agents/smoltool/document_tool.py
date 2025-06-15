
from dotenv import load_dotenv
from smolagents import tool

load_dotenv()


@tool
def get_medical_document(query: str) -> str:
    """Queries and retrieves medical documents, articles, and research papers.

    Args:
        query: the information about the medical symbol .

    Returns:
        str: Retrieved documents or articles in text format.
    """
    print(f"Querying documents with: {query}")
    # Here you would implement the logic to query and retrieve documents
    # For now, we return a placeholder response
    return f"sach Cuu Am chan kinh chapter 1."