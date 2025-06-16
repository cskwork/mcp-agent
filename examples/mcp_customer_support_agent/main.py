import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.router.router_llm_anthropic import RouterLLMAnthropic
from mcp_agent.workflows.swarm.swarm_anthropic import SwarmAnthropic
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

async def basic_customer_support():
    """Basic customer support workflow"""
    app = MCPApp()
    
    # Create customer support agent
    support_agent = Agent(
        name="SupportAgent",
        instructions="""
        You are a professional customer support representative. Your role includes:
        1. Respond to customer inquiries with empathy and professionalism
        2. Search knowledge base and product documentation for solutions
        3. Access order history and account information when needed
        4. Provide step-by-step troubleshooting guidance
        5. Escalate complex issues to human agents with detailed context
        6. Follow up on resolved issues to ensure customer satisfaction
        7. Maintain consistent brand voice and company policies
        """,
        app=app
    )
    
    # Handle customer inquiry
    result = await support_agent.run(
        "Customer email: 'I ordered a product 3 days ago but haven't received shipping confirmation. "
        "My order number is #12345. Can you help me track my order and let me know when it will arrive?'"
    )
    
    print(result)

async def multi_channel_support():
    """Router pattern for multi-channel support"""
    app = MCPApp()
    
    # Create router for different support channels and issue types
    support_router = RouterLLMAnthropic(
        app=app,
        instructions="Route customer support requests to appropriate specialists",
        categories={
            "technical_support": "Technical issues, bugs, and troubleshooting",
            "billing_orders": "Billing questions, order status, and payment issues",
            "product_info": "Product questions, features, and compatibility",
            "account_management": "Account settings, passwords, and profile updates",
            "returns_refunds": "Return requests, refund processing, and exchanges"
        },
        agents={
            "technical_support": Agent(
                name="TechSupport",
                instructions="Technical support specialist for troubleshooting and bug reports",
                app=app
            ),
            "billing_orders": Agent(
                name="BillingSupport", 
                instructions="Billing and order management specialist",
                app=app
            ),
            "product_info": Agent(
                name="ProductExpert",
                instructions="Product knowledge expert and sales support",
                app=app
            ),
            "account_management": Agent(
                name="AccountManager",
                instructions="Account management and user experience specialist",
                app=app
            ),
            "returns_refunds": Agent(
                name="ReturnsProcessor",
                instructions="Returns, refunds, and exchange specialist",
                app=app
            )
        }
    )
    
    # Handle various support requests
    support_requests = [
        "My app keeps crashing when I try to upload files",
        "I was charged twice for my subscription this month",
        "What's the difference between your Pro and Enterprise plans?",
        "I forgot my password and can't access my account",
        "I want to return an item I bought last week"
    ]
    
    results = []
    for request in support_requests:
        result = await support_router.run(request)
        results.append(result)
    
    return results

async def escalation_management():
    """Swarm pattern for escalation management"""
    app = MCPApp()
    
    # Create support team with escalation capabilities
    tier1_agent = Agent(
        name="Tier1Support",
        instructions="""
        First-level support agent handling common inquiries:
        - Password resets and account access
        - Basic product information
        - Order status and shipping
        - Simple troubleshooting
        Escalate to Tier2 if issue requires deeper technical knowledge.
        """,
        app=app
    )
    
    tier2_agent = Agent(
        name="Tier2Support",
        instructions="""
        Advanced technical support specialist:
        - Complex troubleshooting and debugging
        - Integration and API issues
        - Advanced product configuration
        - Performance and scalability concerns
        Escalate to Specialist if issue requires product team involvement.
        """,
        app=app
    )
    
    specialist_agent = Agent(
        name="ProductSpecialist",
        instructions="""
        Product team specialist for critical issues:
        - Product bugs and feature requests
        - Architecture and design questions
        - Custom implementation guidance
        - Critical customer escalations
        """,
        app=app
    )
    
    # Create swarm for intelligent escalation
    support_swarm = SwarmAnthropic(
        app=app,
        agents=[tier1_agent, tier2_agent, specialist_agent],
        instructions="""
        Handle customer support with intelligent escalation:
        1. Start with Tier1 for initial assessment
        2. Escalate to Tier2 for technical issues
        3. Escalate to Specialist for critical/complex issues
        4. Maintain context throughout escalation chain
        """
    )
    
    result = await support_swarm.run(
        "Customer reports: 'Our production API integration is failing with 500 errors "
        "since yesterday. This is affecting our entire user base. We're a Enterprise customer "
        "and need immediate assistance. Error logs show timeout issues with authentication.'"
    )
    
    return result

async def high_volume_support():
    """Parallel processing for high volume"""
    app = MCPApp()
    
    # Create parallel processing for multiple simultaneous requests
    parallel_support = ParallelLLM(
        app=app,
        instructions="Process multiple customer support requests simultaneously",
        agents=[
            Agent(name=f"SupportAgent{i}", app=app, 
                  instructions="Handle customer inquiries professionally and efficiently")
            for i in range(5)  # 5 parallel agents
        ]
    )
    
    # Batch process multiple customer requests
    customer_requests = [
        "How do I reset my password?",
        "My order hasn't arrived yet, can you check status?",
        "I'm getting an error when trying to upload files",
        "Can you help me upgrade my subscription?",
        "I need to cancel my account",
        "The mobile app won't sync my data",
        "I was charged for a service I didn't order",
        "How do I export my data?",
        "Can you help me set up SSO integration?",
        "I need help with API rate limits"
    ]
    
    results = await parallel_support.run(customer_requests)
    return results

async def main():
    """Main function to run customer support workflows"""
    print("=== MCP Customer Support Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Support, 2: Multi-Channel, 3: Escalation Management, 4: High Volume): ")
    
    if workflow == "1":
        await basic_customer_support()
    elif workflow == "2":
        results = await multi_channel_support()
        for i, result in enumerate(results, 1):
            print(f"Request {i} Result: {result}")
    elif workflow == "3":
        result = await escalation_management()
        print(result)
    elif workflow == "4":
        results = await high_volume_support()
        for i, result in enumerate(results, 1):
            print(f"Support {i} Result: {result}")
    else:
        print("Invalid choice. Running basic support...")
        await basic_customer_support()

if __name__ == "__main__":
    asyncio.run(main())