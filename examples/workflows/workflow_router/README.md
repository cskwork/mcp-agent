# Interactive Modular Agent Router

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Cross-platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com)

A sophisticated system for intelligently routing user requests to specialized agents based on content analysis and intent detection. Built on the MCP (Model Context Protocol) framework, it provides an interactive command-line interface for seamless task routing and execution.

## 🚀 Quick Start

Get up and running in under 2 minutes:

### Windows
```cmd
run.bat
```

### Unix/Linux/Mac
```bash
./run.sh
```

That's it! The scripts handle all setup automatically.

## ✨ Features

- **🤖 Intelligent Routing**: Combines keyword matching with LLM-based analysis
- **🎯 Specialized Agents**: RAG, Slack, Browser, and Playwright agents
- **💬 Interactive CLI**: User-friendly command-line interface
- **⚡ Fast Response**: Keyword-based routing for common patterns
- **🧠 LLM Fallback**: Advanced routing for complex requests
- **🔧 Extensible**: Easy to add new agents and capabilities
- **🌍 Cross-platform**: Windows, macOS, and Linux support

## 🏗️ Architecture

```mermaid
graph TD
    A[User Request] --> B[Interactive CLI]
    B --> C[Modular Agent Router]
    C --> D{Routing Strategy}
    D -->|Keyword Match| E[Direct Agent Selection]
    D -->|Complex Request| F[LLM Analysis]
    E --> G[Agent Execution]
    F --> G
    G --> H[Result Display]

    subgraph "Specialized Agents"
        I[RAG Agent<br/>Document Search]
        J[Slack Agent<br/>Team Communication]
        K[Browser Agent<br/>Web Scraping]
        L[Playwright Agent<br/>Browser Testing]
    end

    G --> I
    G --> J
    G --> K
    G --> L
```

## 🤖 Available Agents

| Agent | Purpose | MCP Servers | Example Requests |
|-------|---------|-------------|-----------------|
| **RAG** | Document retrieval and Q&A | Qdrant, Filesystem | "Find documentation about APIs", "Search knowledge base" |
| **Slack** | Team communication | Slack | "Send message to team", "Notify the channel" |
| **Browser** | Web scraping and automation | Puppeteer | "Screenshot website", "Scrape product data" |
| **Playwright** | Advanced browser testing | Playwright | "Test login flow", "Cross-browser validation" |

## 📋 Prerequisites

### Required
- **Python 3.8+** - Core runtime
- **API Keys** - Anthropic (required), OpenAI (optional)

### Optional (for full functionality)
- **Node.js & npm** - For browser and Slack agents
- **uv/uvx** - For Python MCP servers (RAG agent)
- **Docker** - For Qdrant (RAG agent)

## 🔧 Installation

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd interactive-modular-agent-router

# Run automated setup
./run.sh    # Unix/Linux/Mac
run.bat     # Windows
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ../../../  # Local mcp-agent
pip install anthropic openai rich

# Set up configuration
cp config/secrets.example.yaml mcp_agent.secrets.yaml
# Edit mcp_agent.secrets.yaml with your API keys

# Run the application
python main.py
```

## ⚙️ Configuration

### API Keys
Edit `mcp_agent.secrets.yaml`:
```yaml
anthropic:
  api_key: your_anthropic_api_key_here

openai:  # Optional
  api_key: your_openai_api_key_here

# Optional: For Slack agent
SLACK_BOT_TOKEN: xoxb-your-slack-bot-token
SLACK_TEAM_ID: your-team-id
```

### MCP Servers
Individual server configurations in `config/mcp-servers/`:
- `rag.yaml` - Qdrant vector database settings
- `slack.yaml` - Slack integration settings
- `browser.yaml` - Puppeteer browser settings
- `playwright.yaml` - Playwright testing settings

## 📖 Usage Examples

### Interactive Mode
```bash
$ python main.py

🚀 Interactive Modular Agent Router
간단하고 똑똑한 에이전트 라우터입니다!

┌─ Main Menu ─────────────────────────────────────┐
│ 1. 요청 처리 / Process Request                    │
│ 2. 에이전트 목록 / List Agents                    │
│ 3. 요청 분석 / Analyze Request                    │
│ 4. 종료 / Exit                                  │
└────────────────────────────────────────────────┘

Enter your request: Find documentation about APIs
✅ Routed to: rag (method: keyword)
```

### Programmatic Usage
```python
from src.routing.simple_router import SimpleRouter

# Initialize router
router = SimpleRouter()

# Route a request - 3 ways
agent_name, method = await router.route("search for docs", method="smart")
agent_name = router.route_by_keywords("send slack message")  
agent_name = router.route_manually("browser")

# Use the selected agent
agent = router.get_agent(agent_name)
async with agent:
    # Execute your task
    pass
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/        # Unit tests
python -m pytest tests/integration/ # Integration tests

# Run with coverage
python -m pytest --cov=src tests/
```

Check your environment:
```bash
python check-env.py
```

## 📁 Project Structure

```
interactive-modular-agent-router/
├── main.py                # Main application
├── src/                   # Source code
│   ├── agents/           # Agent implementations  
│   ├── routing/          # Simple routing logic
│   └── utils/            # Simple utilities
├── config/               # Configuration templates
├── docs/                 # Essential documentation
├── tests/                # Minimal test suite
├── run.sh                # Unix launcher
├── run.bat               # Windows launcher
├── QUICKSTART.md         # 2-minute setup guide
├── GLOSSARY.md           # Tech terms for children
└── ALTERNATIVES.md       # Design decision alternatives
```

## 🔍 Troubleshooting

### Common Issues

**"Missing API key" error**
- Edit `mcp_agent.secrets.yaml` and add your Anthropic API key

**"No agent selected" warning**
- Some agents need external services (Node.js, Qdrant)
- Run `python scripts/check-environment.py` to see what's available

**Permission errors (Unix/Linux/Mac)**
- Make sure run.sh is executable: `chmod +x run.sh`
- May need `sudo` for global npm packages

### Getting Help

- Check the [documentation](docs/) for detailed guides
- Run environment check: `python scripts/check-environment.py`
- Review logs for specific error messages
- Open an issue on GitHub for bugs or feature requests

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Quick Contributing Steps
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest`
5. Submit a pull request

### Adding New Agents
See [Agent Development Guide](docs/architecture/extension-guide.md) for creating custom agents.

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 2 minutes
- [Installation Guide](docs/getting-started/installation.md) - Detailed setup instructions
- [Agent Documentation](docs/agents/) - Individual agent guides
- [Architecture Overview](docs/architecture/) - Technical documentation
- [API Reference](docs/api/) - Programming interface
- [Troubleshooting](docs/troubleshooting/) - Common issues and solutions

## 🛣️ Roadmap

- [ ] **Agent Marketplace** - Plugin system for community agents
- [ ] **Web Interface** - Browser-based UI alongside CLI
- [ ] **Batch Processing** - Handle multiple requests efficiently
- [ ] **Conversation Memory** - Context across multiple interactions
- [ ] **Performance Metrics** - Request routing analytics
- [ ] **Docker Support** - Containerized deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the [MCP Agent Framework](https://github.com/anthropics/mcp-agent)
- Powered by [Anthropic](https://www.anthropic.com/) and [OpenAI](https://openai.com/) LLMs
- UI powered by [Rich](https://github.com/Textualize/rich)
- Special thanks to all contributors

---

**Made with ❤️ by the MCP Agent Team**

[⭐ Star this repo](https://github.com/your-repo) if you find it useful!