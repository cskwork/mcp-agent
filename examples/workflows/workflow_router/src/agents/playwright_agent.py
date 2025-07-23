"""
Playwright Agent for advanced browser automation and testing.
"""
from mcp_agent.agents.agent import Agent


def create_playwright_agent() -> Agent:
    """
    Creates a Playwright agent specialized for advanced browser automation and testing.
    
    Uses Playwright MCP server for sophisticated browser control, testing, and automation.
    Ideal for complex web automation, testing workflows, and advanced browser interactions.
    
    Returns:
        Agent: Configured Playwright agent with Playwright server access
    """
    return Agent(
        name="playwright_agent",
        instruction="""You are a specialized Playwright automation agent with access to advanced browser automation capabilities.
        
        Your capabilities include:
        - Advanced web browser automation across multiple browsers
        - Web application testing and validation
        - Complex user interaction simulation
        - Mobile device and responsive testing
        - Network interception and API testing
        - Advanced screenshot and video recording
        - Cross-browser compatibility testing
        
        When processing requests:
        1. Choose appropriate browser (Chrome, Firefox, Safari, etc.)
        2. Configure browser settings and viewport
        3. Perform complex interactions and validations
        4. Handle advanced scenarios like file uploads, authentication
        5. Provide detailed results and error handling
        
        You excel at:
        - "Test the website functionality..."
        - "Automate the complex workflow..."
        - "Validate the user interface..."
        - "Record a video of the process..."
        - "Test across different browsers..."
        """,
        server_names=["playwright", "fetch"]
    )


# Keywords that indicate Playwright agent should handle the request
PLAYWRIGHT_KEYWORDS = [
    "playwright", "test", "automate", "browser", "automation", "testing",
    "validate", "simulation", "workflow", "interaction", "e2e", "end-to-end",
    "cross-browser", "mobile", "responsive", "recording", "video", "advanced"
]

# Example queries that Playwright agent handles well
PLAYWRIGHT_EXAMPLES = [
    "Test the login workflow across different browsers",
    "Automate the complex checkout process",
    "Validate the responsive design on mobile devices",
    "Record a video of the user registration flow",
    "Test the file upload functionality end-to-end"
]