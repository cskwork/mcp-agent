# Use Case 3: Intelligent Content Research and Creation Agent

## Overview
Build a comprehensive content research agent that gathers information from multiple sources, analyzes trends, and creates high-quality content for various purposes including articles, reports, social media, and marketing materials.

## What It Does
- Researches topics across web sources, databases, and APIs
- Analyzes content trends and competitive landscapes
- Generates original content in multiple formats and styles
- Fact-checks and validates information sources
- Optimizes content for SEO and engagement
- Manages content workflows and publishing schedules

## How to Use It

### 1. Setup Configuration
Create `mcp_agent.config.yaml`:

```yaml
name: "ContentResearchAgent"
llm:
  provider: "anthropic"
  model_name: "claude-3-5-sonnet-20241022"

mcp_servers:
  brave_search:
    command: "mcp-server-brave-search"
    args: ["--api-key", "${BRAVE_API_KEY}"]
    
  wikipedia:
    command: "mcp-server-wikipedia"
    
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "${CONTENT_DIR}"]
    
  github:
    command: "mcp-server-github"
    args: ["--github-personal-access-token", "${GITHUB_TOKEN}"]
    
  slack:
    command: "mcp-server-slack"
    args: ["--slack-bot-token", "${SLACK_BOT_TOKEN}"]
    
  notion:
    command: "mcp-server-notion" 
    args: ["--notion-api-key", "${NOTION_API_KEY}"]
```

### 2. Create Secrets File
Create `mcp_agent.secrets.yaml`:

```yaml
ANTHROPIC_API_KEY: "your-anthropic-key"
BRAVE_API_KEY: "your-brave-search-key"
GITHUB_TOKEN: "your-github-token"
SLACK_BOT_TOKEN: "your-slack-bot-token"
NOTION_API_KEY: "your-notion-key"
CONTENT_DIR: "/path/to/content/directory"
```

### 3. Basic Implementation

```python
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent

async def main():
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

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Orchestrator Pattern for Content Production

```python
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator

async def content_production_pipeline():
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
```

### 5. Parallel Research with Fan-Out Pattern

```python
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

async def parallel_research():
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
```

### 6. Evaluator-Optimizer for Content Quality

```python
from mcp_agent.workflows.evaluator_optimizer.evaluator_optimizer import EvaluatorOptimizer

async def optimized_content_creation():
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
```

## Key Benefits

- **Multi-Source Research**: Aggregate information from web, databases, APIs, and documents
- **Content Quality Assurance**: Automated fact-checking and quality evaluation
- **SEO Optimization**: Built-in search engine optimization capabilities
- **Scalable Production**: Parallel research and orchestrated content workflows
- **Format Flexibility**: Generate articles, social posts, reports, and multimedia content
- **Workflow Integration**: Connect with publishing platforms and content management systems

## Example MCP Servers for Content Research

- `mcp-server-brave-search` - Web search and current information
- `mcp-server-wikipedia` - Encyclopedic knowledge and references
- `mcp-server-github` - Technical documentation and code examples
- `mcp-server-notion` - Content management and collaboration
- `mcp-server-slack` - Team communication and content sharing
- `mcp-server-twitter` - Social media trends and sentiment analysis
- `@modelcontextprotocol/server-filesystem` - Local content storage and management

## Common Content Workflows

1. **Research-to-Publication Pipeline**: Complete workflow from research to published content
2. **Competitive Content Analysis**: Monitor competitor content and identify opportunities
3. **Trend-Based Content Creation**: Generate content based on emerging trends and topics
4. **Multi-Format Content Adaptation**: Repurpose content across different formats and channels
5. **Content Performance Optimization**: Analyze and improve content based on engagement metrics

## Content Types Supported

- **Long-form Articles**: In-depth analysis and thought leadership pieces
- **Social Media Content**: Posts, threads, and engagement-optimized content
- **Technical Documentation**: API docs, tutorials, and how-to guides
- **Marketing Materials**: Sales copy, product descriptions, and promotional content
- **Research Reports**: Data-driven analysis and industry insights
- **Newsletter Content**: Regular updates and curated content collections