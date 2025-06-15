import logging
from dotenv import load_dotenv
from smolagents import tool

load_dotenv()




@tool
def diagnose(query:str) -> str:
    """Diagnose base on medical query.

    Args:
        query: medical query ask about symptoms and medical history.

    Returns:
        str: Insights or analysis of medical in text format.
    """

    return f"you're very healthy ."



