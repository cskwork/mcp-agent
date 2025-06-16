import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM
from mcp_agent.workflows.evaluator_optimizer.evaluator_optimizer import EvaluatorOptimizer

async def basic_content_research():
    """Basic content research workflow"""
    app = MCPApp()
    
    # Create content research agent
    researcher = Agent(
        name="ContentResearcher",
        instructions="""
        You are an expert content researcher and creator. Your responsibilities include:
        1. Conduct thorough research on assigned topics using multiple sources
        2. Analyze information for accuracy, relevance, and credibility
        3. Identify content trends and opportunities
        4. Create engaging, well-structured content in various formats
        5. Optimize content for search engines and target audiences
        6. Fact-check and cite all sources appropriately
        """,
        app=app
    )
    
    # Research and create content
    result = await researcher.run(
        "Research the latest trends in artificial intelligence for business applications. "
        "Create a comprehensive 2000-word article covering key developments, "
        "practical applications, and future predictions. "
        "Include statistics, expert quotes, and actionable insights for business leaders."
    )
    
    print(result)

async def content_production_pipeline():
    """Orchestrator pattern for content production"""
    app = MCPApp()
    
    # Create specialized content team
    orchestrator = Orchestrator(
        app=app,
        instructions="Coordinate comprehensive content creation workflow",
        workers=[
            Agent(
                name="Researcher",
                instructions="""
                Primary researcher focusing on:
                - Gathering information from credible sources
                - Fact-checking and source validation
                - Identifying key statistics and data points
                - Competitive analysis and trend identification
                """,
                app=app
            ),
            Agent(
                name="ContentStrategist", 
                instructions="""
                Content strategy expert responsible for:
                - Content planning and editorial calendars
                - Audience analysis and targeting
                - SEO optimization and keyword research
                - Content performance analysis
                """,
                app=app
            ),
            Agent(
                name="Writer",
                instructions="""
                Professional content writer specializing in:
                - Creating engaging, well-structured content
                - Adapting tone and style for different audiences
                - Crafting compelling headlines and introductions
                - Ensuring clarity and readability
                """,
                app=app
            ),
            Agent(
                name="Editor",
                instructions="""
                Editorial specialist focused on:
                - Content review and quality assurance
                - Grammar, style, and consistency checks
                - Fact verification and source citation
                - Final content optimization
                """,
                app=app
            )
        ]
    )
    
    result = await orchestrator.run(
        "Create a comprehensive content series about sustainable technology innovations. "
        "Include 5 articles, social media posts, and an executive summary. "
        "Target audience: technology executives and decision makers."
    )
    
    return result

async def parallel_research():
    """Parallel research with Fan-Out pattern"""
    app = MCPApp()
    
    # Create parallel research workflow
    parallel_researcher = ParallelLLM(
        app=app,
        instructions="Coordinate parallel research across multiple agents",
        agents=[
            Agent(
                name="TechResearcher",
                instructions="Research technology trends and innovations",
                app=app
            ),
            Agent(
                name="MarketResearcher", 
                instructions="Analyze market data and business trends",
                app=app
            ),
            Agent(
                name="CompetitorAnalyst",
                instructions="Research competitor activities and strategies",
                app=app
            ),
            Agent(
                name="SocialTrendAnalyst",
                instructions="Monitor social media trends and sentiment",
                app=app
            )
        ]
    )
    
    research_queries = [
        "Latest AI developments in healthcare",
        "Enterprise software market trends Q1 2024", 
        "Top competitors in the SaaS analytics space",
        "Social media sentiment around remote work tools"
    ]
    
    results = await parallel_researcher.run(research_queries)
    return results

async def optimized_content_creation():
    """Evaluator-Optimizer for content quality"""
    app = MCPApp()
    
    # Create content with iterative improvement
    optimizer = EvaluatorOptimizer(
        app=app,
        task_agent=Agent(
            name="ContentCreator",
            instructions="Create high-quality content based on requirements",
            app=app
        ),
        evaluator_agent=Agent(
            name="ContentEvaluator", 
            instructions="""
            Evaluate content quality across multiple dimensions:
            - Accuracy and factual correctness
            - Engagement and readability
            - SEO optimization
            - Target audience alignment
            - Competitive positioning
            Provide specific feedback for improvement.
            """,
            app=app
        ),
        max_iterations=3
    )
    
    result = await optimizer.run(
        "Create a blog post about 'The Future of Remote Work Technology'. "
        "Target: 1500 words, professional tone, SEO-optimized for 'remote work tools'."
    )
    
    return result

async def main():
    """Main function to run content research workflows"""
    print("=== MCP Content Research Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Research, 2: Production Pipeline, 3: Parallel Research, 4: Optimized Creation): ")
    
    if workflow == "1":
        await basic_content_research()
    elif workflow == "2":
        result = await content_production_pipeline()
        print(result)
    elif workflow == "3":
        results = await parallel_research()
        for i, result in enumerate(results, 1):
            print(f"Research {i} Result: {result}")
    elif workflow == "4":
        result = await optimized_content_creation()
        print(result)
    else:
        print("Invalid choice. Running basic research...")
        await basic_content_research()

if __name__ == "__main__":
    asyncio.run(main())