# Use Case 1: Intelligent Data Analysis Agent

## Overview
Build an AI agent that connects to multiple data sources and performs comprehensive analysis with visualization capabilities.

## What It Does
- Connects to databases, APIs, and file systems via MCP servers
- Automatically explores datasets and identifies patterns
- Generates insights, visualizations, and reports
- Handles complex multi-step analysis workflows

## How to Use It

### 1. Setup Configuration
Create `mcp_agent.config.yaml`:

```yaml
name: "DataAnalysisAgent"
llm:
  provider: "anthropic"
  model_name: "claude-3-5-sonnet-20241022"
  
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/data"]
  
  database:
    command: "mcp-server-postgres" 
    args: ["--connection-string", "postgresql://user:pass@localhost/db"]
    
  web_scraper:
    command: "mcp-server-brave-search"
    args: ["--api-key", "${BRAVE_API_KEY}"]
```

### 2. Create Secrets File
Create `mcp_agent.secrets.yaml`:

```yaml
ANTHROPIC_API_KEY: "your-anthropic-key"
BRAVE_API_KEY: "your-brave-search-key"
```

### 3. Implementation

```python
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent

async def main():
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

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Advanced Workflow with Orchestrator Pattern

```python
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator

async def advanced_analysis():
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
```

## Key Benefits

- **Multi-source Integration**: Connect to databases, APIs, files, and web sources
- **Automated Analysis**: AI-driven exploration reduces manual work
- **Scalable Workflows**: Orchestrator pattern handles complex multi-step analysis
- **Flexible Output**: Generate reports, visualizations, or raw insights
- **Composable**: Chain with other workflows for end-to-end data pipelines

## Example MCP Servers for Data Analysis

- `@modelcontextprotocol/server-filesystem` - File system access
- `mcp-server-postgres` - PostgreSQL database
- `mcp-server-sqlite` - SQLite database  
- `mcp-server-brave-search` - Web search and data gathering
- `mcp-server-github` - Repository data analysis
- `mcp-server-slack` - Communication data analysis