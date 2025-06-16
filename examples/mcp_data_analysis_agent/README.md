# Intelligent Data Analysis Agent

## Overview
Build an AI agent that connects to multiple data sources and performs comprehensive analysis with visualization capabilities.

## What It Does
- Connects to databases, APIs, and file systems via MCP servers
- Automatically explores datasets and identifies patterns
- Generates insights, visualizations, and reports
- Handles complex multi-step analysis workflows

## Setup

1. Copy secrets file:
```bash
cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
```

2. Add your API keys to `mcp_agent.secrets.yaml`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the agent:
```bash
uv run main.py
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