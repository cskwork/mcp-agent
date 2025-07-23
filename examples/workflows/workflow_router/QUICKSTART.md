# Interactive Modular Agent Router - Quick Start

Get the Interactive Modular Agent Router running in under 2 minutes! 🚀

## One-Command Start

### Windows
```cmd
run.bat
```

### Unix/Linux/Mac
```bash
./run.sh
```

That's it! The scripts handle everything automatically.

## What You Get

An interactive CLI that intelligently routes your requests to specialized agents:

- **RAG Agent** - Search documents and knowledge bases
- **Slack Agent** - Send messages and manage team communication  
- **Browser Agent** - Web scraping and basic automation
- **Playwright Agent** - Advanced browser testing and automation

## Prerequisites

The run scripts will check and guide you through installing:

### Required
- **Python 3.8+** - Core runtime
- **API Keys** - Anthropic (required), OpenAI (optional)

### Optional (for full functionality)
- **Node.js** - For browser and Slack agents
- **uv/uvx** - For Python MCP servers (RAG agent)
- **Qdrant** - Vector database for RAG (if using document search)

## Quick Setup

1. **Clone and navigate:**
   ```bash
   git clone <repository>
   cd mcp-agent/examples/workflows/workflow_router
   ```

2. **Run the setup:**
   ```bash
   # Windows
   run.bat
   
   # Unix/Linux/Mac  
   ./run.sh
   ```

3. **Add your API key:**
   - The script will create `mcp_agent.secrets.yaml`
   - Add your Anthropic API key (get one at https://console.anthropic.com)
   - Optionally add OpenAI key for additional routing options

4. **Start using:**
   - Enter requests like "search for documentation"
   - Watch as they get routed to the best agent
   - Choose to execute or just analyze

## Example Requests

Try these in the interactive CLI:

```
Find documents about machine learning
Send a message to the development team  
Take a screenshot of https://example.com
Test the login workflow on Chrome
Scrape product data from the website
```

## Troubleshooting

### "Missing API key" error
- Edit `mcp_agent.secrets.yaml` 
- Add your Anthropic API key under `anthropic: api_key: your_key_here`

### "No agent selected" warning
- Some agents need external services (Node.js, Qdrant)
- The script shows what's available vs missing
- Basic routing still works with just Python + API key

### Permission errors (Unix/Linux/Mac)
- Make sure run.sh is executable: `chmod +x run.sh`
- May need `sudo` for global npm packages

## Advanced Setup

### Full RAG Agent Support
```bash
# Install and start Qdrant
docker run -p 6333:6333 qdrant/qdrant
# or install locally from https://qdrant.tech
```

### Slack Agent Setup
1. Create a Slack app at https://api.slack.com/apps
2. Get Bot User OAuth Token and Team ID
3. Add to `mcp_agent.secrets.yaml`:
   ```yaml
   SLACK_BOT_TOKEN: xoxb-your-token
   SLACK_TEAM_ID: your-team-id
   ```

## What the Run Scripts Do

1. ✅ Check Python, Node.js, and tool availability
2. 🔧 Create and activate virtual environment
3. 📦 Install all Python dependencies
4. ⚙️ Set up configuration files
5. 🔑 Guide you through API key setup
6. 🌐 Install MCP servers (Node.js packages)
7. 🚀 Launch the interactive application

## Manual Installation (if needed)

If the run scripts don't work for your setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ../../../  # Local mcp-agent
pip install anthropic openai rich

# Install MCP servers (optional)
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-puppeteer

# Set up config
cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
# Edit mcp_agent.secrets.yaml with your API keys

# Run
python modular_main.py
```

## Need Help?

- Check the console output for specific error messages
- Ensure all API keys are properly configured
- Verify external services (Qdrant, etc.) are running if needed
- Visit https://github.com/anthropics/mcp-agent for detailed documentation

Happy routing! 🤖