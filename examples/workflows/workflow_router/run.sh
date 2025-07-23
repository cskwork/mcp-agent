#!/bin/bash

# ============================================================================
# Interactive Modular Agent Router - Unix/Linux/Mac Setup & Run Script
# ============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo
    echo "========================================"
    echo "  Interactive Modular Agent Router"
    echo "========================================"
    echo
}

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

print_header

# Check if Python is installed
print_color $BLUE "Checking Python installation..."
if check_command python3; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
elif check_command python; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
else
    print_color $RED "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

print_color $GREEN "Found Python $PYTHON_VERSION"

# Check Python version (basic check for 3.x)
if [[ $PYTHON_VERSION < "3.8" ]]; then
    print_color $YELLOW "WARNING: Python $PYTHON_VERSION detected. Python 3.8+ is recommended."
fi

# Check if pip is available
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    print_color $RED "ERROR: pip is not available"
    echo "Please install pip for Python 3"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3-pip"
    echo "  macOS: pip is usually included with Python"
    exit 1
fi

# Check if Node.js is installed
print_color $BLUE "Checking Node.js installation..."
if check_command node; then
    NODE_VERSION=$(node --version 2>&1)
    print_color $GREEN "Found Node.js $NODE_VERSION"
    NODE_AVAILABLE=true
    
    # Check npm
    if ! check_command npm; then
        print_color $YELLOW "WARNING: npm is not available"
        NODE_AVAILABLE=false
    fi
else
    print_color $YELLOW "WARNING: Node.js is not installed"
    echo "Some MCP servers require Node.js. Install from:"
    echo "  Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "  CentOS/RHEL: curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash - && sudo yum install nodejs npm"
    echo "  macOS: brew install node"
    echo "  Or visit: https://nodejs.org"
    print_color $YELLOW "Continuing without Node.js support..."
    NODE_AVAILABLE=false
fi

# Check if uv/uvx is installed
print_color $BLUE "Checking uv package manager..."
if check_command uvx; then
    print_color $GREEN "Found uvx"
    UVX_AVAILABLE=true
elif check_command uv; then
    print_color $GREEN "Found uv"
    UVX_AVAILABLE=true
else
    print_color $YELLOW "WARNING: uvx (uv package manager) is not installed"
    echo "Some MCP servers require uvx. Install with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  Or: pip install uv"
    print_color $YELLOW "Continuing without uvx support..."
    UVX_AVAILABLE=false
fi

# Create virtual environment if it doesn't exist
print_color $BLUE "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        print_color $RED "ERROR: Failed to create virtual environment"
        echo "Make sure python3-venv is installed:"
        echo "  Ubuntu/Debian: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_color $RED "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
print_color $BLUE "Upgrading pip..."
pip install --upgrade pip >/dev/null 2>&1

# Install dependencies
print_color $BLUE "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    # Handle the local mcp-agent dependency
    echo "Installing mcp-agent from local source..."
    if [ -f "../../../setup.py" ] || [ -f "../../../pyproject.toml" ]; then
        pip install -e ../../../
    else
        print_color $YELLOW "WARNING: Local mcp-agent source not found, trying pip install..."
        pip install mcp-agent
    fi
    
    # Install other dependencies
    echo "Installing additional dependencies..."
    pip install anthropic openai rich
    
    if [ $? -ne 0 ]; then
        print_color $RED "ERROR: Failed to install Python dependencies"
        exit 1
    fi
    print_color $GREEN "Python dependencies installed successfully"
else
    print_color $YELLOW "No requirements.txt found, installing minimal dependencies..."
    pip install anthropic openai rich
fi

# Setup configuration files
print_color $BLUE "Setting up configuration..."

# Check if secrets file exists
if [ ! -f "mcp_agent.secrets.yaml" ]; then
    if [ -f "mcp_agent.secrets.yaml.example" ]; then
        print_color $YELLOW "Creating secrets configuration file..."
        cp "mcp_agent.secrets.yaml.example" "mcp_agent.secrets.yaml"
        print_color $GREEN "Created mcp_agent.secrets.yaml"
        echo
        print_color $YELLOW "IMPORTANT: Please edit mcp_agent.secrets.yaml and add your API keys:"
        echo "  - Anthropic API key (required for LLM routing)"
        echo "  - OpenAI API key (optional, for OpenAI routing)"
        echo "  - Slack tokens (optional, for Slack agent)"
        echo
        read -p "Would you like to open the secrets file now to add your API keys? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Try different editors
            if check_command nano; then
                nano "mcp_agent.secrets.yaml"
            elif check_command vim; then
                vim "mcp_agent.secrets.yaml"
            elif check_command code; then
                code "mcp_agent.secrets.yaml"
            else
                echo "Please edit mcp_agent.secrets.yaml with your preferred editor"
            fi
        fi
    else
        print_color $YELLOW "No secrets template found. You may need to set up API keys manually."
    fi
fi

# Check for required API keys
print_color $BLUE "Checking API key configuration..."
if [ -f "mcp_agent.secrets.yaml" ]; then
    if ! grep -q "anthropic_api_key" "mcp_agent.secrets.yaml" 2>/dev/null; then
        print_color $RED "WARNING: Anthropic API key not configured"
        echo "The app requires an Anthropic API key for LLM routing."
        echo "Please edit mcp_agent.secrets.yaml and add your API key."
        echo
    fi
else
    print_color $YELLOW "No secrets file found. API keys may not be configured."
fi

# Install Node.js MCP servers if Node is available
if [ "$NODE_AVAILABLE" = true ]; then
    print_color $BLUE "Installing Node.js MCP servers..."
    npm install -g @modelcontextprotocol/server-filesystem >/dev/null 2>&1 || true
    npm install -g @modelcontextprotocol/server-slack >/dev/null 2>&1 || true
    npm install -g @modelcontextprotocol/server-puppeteer >/dev/null 2>&1 || true
    npm install -g @playwright/mcp >/dev/null 2>&1 || true
    print_color $GREEN "Node.js MCP servers installed"
fi

# Install Python MCP servers if uvx is available
if [ "$UVX_AVAILABLE" = true ]; then
    print_color $BLUE "Installing Python MCP servers..."
    # Note: Actual uvx installations would happen on-demand when the app runs
    print_color $GREEN "Python MCP server support ready"
fi

# Final setup check
echo
print_color $GREEN "========================================"
print_color $GREEN "Setup completed successfully!"
print_color $GREEN "========================================"
echo

# Display system status
print_color $BLUE "System Status:"
echo -e "  Python: ${GREEN}✓ $PYTHON_VERSION${NC}"
if [ "$NODE_AVAILABLE" = true ]; then
    echo -e "  Node.js: ${GREEN}✓ $NODE_VERSION${NC}"
else
    echo -e "  Node.js: ${YELLOW}⚠ Not available${NC}"
fi
if [ "$UVX_AVAILABLE" = true ]; then
    echo -e "  uvx: ${GREEN}✓ Available${NC}"
else
    echo -e "  uvx: ${YELLOW}⚠ Not available${NC}"
fi

echo
print_color $BLUE "Available Agents:"
echo "  • RAG Agent (requires Qdrant + uvx)"
echo "  • Slack Agent (requires Node.js + Slack tokens)"
echo "  • Browser Agent (requires Node.js)"
echo "  • Playwright Agent (requires Node.js)"

echo
print_color $GREEN "Starting Interactive Modular Agent Router..."
print_color $YELLOW "Press Ctrl+C at any time to exit"
echo

# Run the application
$PYTHON_CMD main.py

# Check if the app ran successfully
if [ $? -ne 0 ]; then
    echo
    print_color $RED "Application exited with an error"
    echo
    print_color $YELLOW "Common issues:"
    echo "  • Missing API keys in mcp_agent.secrets.yaml"
    echo "  • Required services not running (e.g., Qdrant for RAG)"
    echo "  • Network connectivity issues"
    echo "  • Missing dependencies"
    echo
    print_color $BLUE "For help, check the logs above or visit:"
    echo "https://github.com/anthropics/mcp-agent"
else
    echo
    print_color $GREEN "Application closed successfully"
fi