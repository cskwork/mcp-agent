# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Linting and Formatting
- `uv run python scripts/lint.py` - Run linting checks with ruff
- `uv run python scripts/lint.py --fix` - Run linting with auto-fix
- `uv run python scripts/format.py` - Format code with ruff
- `uv run python scripts/lint.py --watch` - Watch mode for continuous linting

### Testing
- `uv run python -m pytest tests/` - Run all tests
- `uv run python -m pytest tests/test_event_progress.py` - Run specific test

### Running Examples
Examples are in the `/examples` directory. To run an example:
```bash
cd examples/mcp_basic_agent  # Or any other example
cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml  # Add your API keys
uv run main.py
```

### Package Management
- `uv add <package>` - Add dependency (this project uses uv)
- `uv lock` - Update lock file
- `uv sync` - Install dependencies

## Core Architecture

### Framework Structure
**mcp-agent** is a Python framework for building AI agents using the Model Context Protocol (MCP). The architecture is built around these core components:

1. **MCPApp** (`src/mcp_agent/app.py`) - Main application class managing global state and configuration
2. **Agent** (`src/mcp_agent/agents/agent.py`) - Entities with access to MCP servers, extending MCPAggregator
3. **AugmentedLLM** (`src/mcp_agent/workflows/llm/augmented_llm.py`) - LLMs enhanced with MCP server tools
4. **Workflows** (`src/mcp_agent/workflows/`) - Composable patterns implementing Anthropic's "Building Effective Agents" patterns

### Key Patterns
- **Parallel** - Fan-out to multiple sub-agents, fan-in results
- **Router** - Route inputs to relevant categories/agents using embeddings or LLM classification
- **Orchestrator-Workers** - Higher-level LLM plans and assigns work to sub-agents
- **Evaluator-Optimizer** - Iterative refinement with quality evaluation
- **Swarm** - Model-agnostic implementation of OpenAI's Swarm pattern

### MCP Integration
- **gen_client** (`src/mcp_agent/mcp/gen_client.py`) - Manages MCP server lifecycle
- **MCPConnectionManager** (`src/mcp_agent/mcp/mcp_connection_manager.py`) - Persistent server connections
- **MCPAggregator** (`src/mcp_agent/mcp/mcp_aggregator.py`) - Single interface for multiple MCP servers

### Configuration
- `mcp_agent.config.yaml` - Main configuration (can be committed)
- `mcp_agent.secrets.yaml` - API keys and secrets (gitignored)
- Schema validation in `schema/mcp-agent.config.schema.json`

### Execution Patterns
- All workflows are async and use context managers
- Everything is composable - workflows can be chained together
- Built-in support for human input and signaling via `human_input/`
- Durable execution support via Temporal integration (`executor/temporal.py`)

### Logging and Monitoring
- Rich logging with structured events (`logging/`)
- Progress display and event tracking (`progress_display.py`, `event_progress.py`)
- Telemetry and usage tracking (`telemetry/`)

## Development Notes

### Adding New Workflows
New workflow patterns should:
1. Extend `AugmentedLLM` for composability
2. Use async context managers for resource management
3. Support both programmatic and YAML configuration
4. Include examples in `/examples` directory

### MCP Server Integration
When adding MCP server support:
1. Add server configuration to `mcp_agent.config.yaml`
2. Use `MCPAggregator` for multi-server access
3. Handle server lifecycle with `gen_client` or `MCPConnectionManager`

### Testing
Tests use a gold master approach with fixture data. Test files are in `/tests` with fixtures in `/tests/fixture/`.

### CLI Interface
The framework provides multiple CLI entry points:
- `mcp-agent`
- `mcp_agent` 
- `mcpagent`
- `silsila` (easter egg reference)