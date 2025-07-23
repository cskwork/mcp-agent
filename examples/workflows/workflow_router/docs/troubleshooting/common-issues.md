# Common Issues and Solutions

This guide covers the most frequently encountered issues and their solutions.

## 🔑 API Key Issues

### "Missing API key" Error

**Problem:** Application fails to start or route requests due to missing API key.

**Solutions:**
1. **Check secrets file exists:**
   ```bash
   ls -la mcp_agent.secrets.yaml
   ```

2. **Verify API key format:**
   ```yaml
   # Correct format:
   anthropic:
     api_key: sk-ant-api03-your-actual-key-here
   
   # Wrong (still template):
   anthropic:
     api_key: anthropic_api_key
   ```

3. **Create secrets file from template:**
   ```bash
   cp config/secrets.example.yaml mcp_agent.secrets.yaml
   # Then edit with your real API key
   ```

### "Invalid API key" Error

**Problem:** API key is present but rejected by the service.

**Solutions:**
1. **Verify key validity:**
   - Check Anthropic Console for key status
   - Ensure key hasn't expired
   - Confirm key has proper permissions

2. **Test key manually:**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        -H "Content-Type: application/json" \
        https://api.anthropic.com/v1/messages
   ```

## 🛠️ Installation Issues

### Python Virtual Environment Problems

**Problem:** Virtual environment creation or activation fails.

**Solutions:**
1. **Install venv module (Ubuntu/Debian):**
   ```bash
   sudo apt install python3-venv
   ```

2. **Recreate virtual environment:**
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # Unix
   venv\Scripts\activate     # Windows
   ```

3. **Use different Python version:**
   ```bash
   # Try python3 instead of python
   python3 -m venv venv
   ```

### Dependency Installation Failures

**Problem:** pip install fails for required packages.

**Solutions:**
1. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install with verbose output:**
   ```bash
   pip install -v anthropic openai rich
   ```

3. **Use specific package versions:**
   ```bash
   pip install anthropic==0.7.* openai>=1.0.0 rich>=13.0.0
   ```

### Node.js and MCP Server Issues

**Problem:** MCP servers fail to install or run.

**Solutions:**
1. **Check Node.js version:**
   ```bash
   node --version  # Should be 16+
   npm --version
   ```

2. **Install Node.js (if missing):**
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # macOS
   brew install node
   
   # Windows
   # Download from nodejs.org
   ```

3. **Clear npm cache:**
   ```bash
   npm cache clean --force
   ```

4. **Install MCP servers locally:**
   ```bash
   # Instead of -g flag
   npm install @modelcontextprotocol/server-filesystem
   ```

## 🔄 Runtime Issues

### "No agent selected" Warning

**Problem:** Router cannot find appropriate agent for request.

**Solutions:**
1. **Check agent keywords:**
   - Use specific terms like "search", "slack", "browser"
   - Try the "Analyze Request" option to see keyword scores

2. **Verify MCP servers are running:**
   ```bash
   python scripts/check-environment.py
   ```

3. **Try more specific requests:**
   ```
   # Instead of: "help me"
   # Try: "search for documentation"
   ```

### Agent Connection Failures

**Problem:** Selected agent fails to connect or execute.

**Solutions:**
1. **Check external services:**
   - Qdrant running (for RAG): `docker ps | grep qdrant`
   - Network connectivity
   - Service status

2. **Verify MCP server configuration:**
   ```bash
   # Check config files
   ls -la config/mcp-servers/
   cat config/mcp-servers/rag.yaml
   ```

3. **Test MCP servers individually:**
   ```bash
   # Test Qdrant connection
   curl http://localhost:6333/health
   ```

### Import or Module Errors

**Problem:** Python import errors when running the application.

**Solutions:**
1. **Verify virtual environment is activated:**
   ```bash
   which python  # Should show venv path
   ```

2. **Check Python path:**
   ```python
   import sys
   print(sys.path)
   ```

3. **Install missing dependencies:**
   ```bash
   pip install -e ../../../  # Local mcp-agent
   pip install -r requirements.txt
   ```

## 🖥️ Platform-Specific Issues

### Windows

**Problem:** Permission errors or script execution issues.

**Solutions:**
1. **Run as Administrator:**
   - Right-click Command Prompt → "Run as administrator"

2. **Enable script execution:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Use PowerShell instead of CMD:**
   - PowerShell has better Unicode and path handling

### macOS

**Problem:** Permission denied or certificate issues.

**Solutions:**
1. **Install certificates:**
   ```bash
   /Applications/Python\ 3.x/Install\ Certificates.command
   ```

2. **Use Homebrew Python:**
   ```bash
   brew install python@3.11
   # Use /opt/homebrew/bin/python3 instead of system python
   ```

### Linux

**Problem:** Missing system dependencies.

**Solutions:**
1. **Install build essentials (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install build-essential python3-dev
   ```

2. **Install additional libraries:**
   ```bash
   sudo apt install libssl-dev libffi-dev python3-venv
   ```

## 🔍 Debugging Tips

### Enable Verbose Logging

Add to your configuration:
```yaml
logger:
  level: debug
  type: console
```

### Check Environment Status

```bash
# Run comprehensive environment check
python scripts/check-environment.py

# Check specific components
python -c "import anthropic; print('Anthropic OK')"
python -c "import openai; print('OpenAI OK')"
python -c "import rich; print('Rich OK')"
```

### Test Individual Components

```python
# Test router initialization
from src.routing.router import ModularAgentRouter
router = ModularAgentRouter()
print(router.get_available_agents())

# Test agent creation
from src.agents.rag_agent import create_rag_agent
agent = create_rag_agent()
print(agent.name)
```

## 📞 Getting Additional Help

If these solutions don't resolve your issue:

1. **Check console output carefully** - Error messages often contain the solution
2. **Run environment diagnostics:** `python scripts/check-environment.py`
3. **Search existing GitHub issues** for similar problems
4. **Open a new issue** with:
   - Your operating system and version
   - Python version (`python --version`)
   - Complete error message
   - Steps to reproduce
   - Output of environment check script

## 📚 Related Documentation

- [Installation Guide](../getting-started/installation.md)
- [Configuration Problems](configuration-problems.md)
- [Agent-Specific Issues](agent-specific-issues.md)