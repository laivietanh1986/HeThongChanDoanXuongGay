
from dotenv import load_dotenv
from smolagents import tool

load_dotenv()



@tool
def scrape_page_with_jina_ai(url: str) -> str:
    """Scrapes content from a webpage using Jina AI's web scraping service.

    Args:
        url: The URL of the webpage to scrape. Must be a valid web address to extract content from.

    Returns:
        str: The scraped content in markdown format.
    """
    print(f"Scraping Jina AI..: {url}")
    # response = requests.get("https://r.jina.ai/" + url, headers=headers)
    response = requests.get("https://r.jina.ai/" + url)

    markdown_content = response.text

    return markdown_content
@tool
def radiology_tool(image_path: str) -> str:
    """Analyzes a radiology image and provides insights.

    Args:
        image_path: The path to the radiology image file.

    Returns:
        str: Insights or analysis of the radiology image.
    """
    print(f"Analyzing radiology image at: {image_path}")
    # Here you would implement the logic to analyze the image
    # For now, we return a placeholder response
    return f"you have uploaded a radiology image at {image_path}. the result is : you're very healthy ."