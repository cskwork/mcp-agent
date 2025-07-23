"""
Slack Agent for team communication and messaging integration.
"""
from mcp_agent.agents.agent import Agent


def create_slack_agent() -> Agent:
    """
    Creates a Slack agent specialized for team communication and messaging.
    
    Uses Slack MCP server for sending messages, managing channels, and team interactions.
    Ideal for communication tasks, notifications, and team collaboration.
    
    Returns:
        Agent: Configured Slack agent with Slack server access
    """
    return Agent(
        name="slack_agent",
        instruction="""You are a specialized Slack integration agent with access to Slack workspace functionality.
        
        Your capabilities include:
        - Sending messages to channels and users
        - Reading channel history and messages
        - Managing Slack channels and conversations
        - Team notifications and alerts
        - Slack workflow automation
        
        When processing requests:
        1. Identify the target channel or user
        2. Format messages appropriately for Slack
        3. Handle mentions, links, and formatting
        4. Provide confirmation of message delivery
        5. Respect channel permissions and guidelines
        
        You excel at:
        - "Send a message to..."
        - "Notify the team about..."
        - "Post to #channel..."
        - "Update the status in Slack"
        - "Alert the developers that..."
        """,
        server_names=["slack"]
    )


# Keywords that indicate Slack agent should handle the request
SLACK_KEYWORDS = [
    "slack", "message", "send", "notify", "alert", "post", "channel",
    "team", "communicate", "dm", "direct message", "mention", "ping",
    "announcement", "update", "status", "chat", "conversation"
]

# Example queries that Slack agent handles well
SLACK_EXAMPLES = [
    "Send a message to the development channel",
    "Notify the team about the deployment completion",
    "Post the meeting notes to #general",
    "Alert @john about the urgent bug fix",
    "Send a status update to the project channel"
]