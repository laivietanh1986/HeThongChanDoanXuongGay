
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
    return f"book name Cuu Am chan kinh chapter 1. the content of book is with the fracture in hand, the fracture position is thumb fracture. to the treatment is using ice , the recovery time will be 2 months ."