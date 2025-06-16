import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator

async def basic_data_analysis():
    """Basic data analysis workflow"""
    app = MCPApp()
    
    # Create data analysis agent
    agent = Agent(
        name="DataAnalyst",
        instructions="""
        You are a data analysis expert. When given a dataset or data source:
        1. Explore the data structure and schema
        2. Identify key patterns, outliers, and trends
        3. Generate relevant visualizations
        4. Provide actionable insights and recommendations
        5. Create a comprehensive analysis report
        """,
        app=app
    )
    
    # Analyze sales data
    result = await agent.run(
        "Analyze the Q4 sales data in /data/sales_q4.csv. "
        "Focus on regional performance, product trends, and growth opportunities. "
        "Create visualizations and a summary report."
    )
    
    print(result)

async def advanced_analysis():
    """Advanced workflow with Orchestrator pattern"""
    app = MCPApp()
    
    # Create orchestrator with specialized workers
    orchestrator = Orchestrator(
        app=app,
        instructions="Coordinate comprehensive data analysis",
        workers=[
            Agent(
                name="DataExplorer", 
                instructions="Explore data structure and quality",
                app=app
            ),
            Agent(
                name="StatisticalAnalyst",
                instructions="Perform statistical analysis and hypothesis testing", 
                app=app
            ),
            Agent(
                name="VisualizationSpecialist",
                instructions="Create charts, graphs, and interactive visualizations",
                app=app
            ),
            Agent(
                name="ReportWriter",
                instructions="Synthesize findings into executive summary",
                app=app
            )
        ]
    )
    
    result = await orchestrator.run(
        "Perform comprehensive analysis of customer churn data. "
        "Identify key factors, build predictive insights, and recommend actions."
    )
    
    return result

async def main():
    """Main function to run data analysis workflows"""
    print("=== MCP Data Analysis Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Analysis, 2: Advanced Analysis): ")
    
    if workflow == "1":
        await basic_data_analysis()
    elif workflow == "2":
        result = await advanced_analysis()
        print(result)
    else:
        print("Invalid choice. Running basic analysis...")
        await basic_data_analysis()

if __name__ == "__main__":
    asyncio.run(main())