"""
Browser Agent for web scraping and browser automation using Puppeteer.
"""
from mcp_agent.agents.agent import Agent


def create_browser_agent() -> Agent:
    """
    Creates a browser agent specialized for web scraping and browser automation.
    
    Uses Puppeteer MCP server for browser control, page navigation, and content extraction.
    Ideal for web scraping, form automation, and basic browser interactions.
    
    Returns:
        Agent: Configured browser agent with Puppeteer server access
    """
    return Agent(
        name="browser_agent",
        instruction="""You are a specialized browser automation agent with access to Puppeteer for web scraping and browser control.
        
        Your capabilities include:
        - Web page navigation and content extraction
        - Form filling and submission
        - Taking screenshots of web pages
        - Basic browser automation tasks
        - HTML parsing and data extraction
        - Cookie and session management
        
        When processing requests:
        1. Navigate to the target website
        2. Wait for page elements to load
        3. Extract required information or perform actions
        4. Handle dynamic content and JavaScript rendering
        5. Return structured data or confirmation of actions
        
        You excel at:
        - "Scrape data from website..."
        - "Take a screenshot of..."
        - "Fill out the form on..."
        - "Extract information from..."
        - "Navigate to... and get..."
        """,
        server_names=["puppeteer", "fetch"]
    )


# Keywords that indicate Browser agent should handle the request
BROWSER_KEYWORDS = [
    "scrape", "website", "web", "browser", "navigate", "screenshot",
    "extract", "crawl", "page", "html", "form", "submit", "click",
    "automation", "puppeteer", "visit", "fetch", "download", "capture"
]

# Example queries that Browser agent handles well
BROWSER_EXAMPLES = [
    "Scrape product prices from the e-commerce website",
    "Take a screenshot of the homepage",
    "Extract contact information from the company website",
    "Fill out the registration form automatically",
    "Navigate to the news site and get the latest headlines"
]