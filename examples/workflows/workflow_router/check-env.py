#!/usr/bin/env python3
"""
Environment Check Script for Interactive Modular Agent Router

This script checks if your system has all the required dependencies and configuration
to run the Interactive Modular Agent Router successfully.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colors for cross-platform output
class Colors:
    if platform.system() == "Windows":
        # Windows cmd doesn't support ANSI by default, but modern Windows Terminal does
        try:
            import colorama
            colorama.init()
            RED = '\033[91m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            BLUE = '\033[94m'
            BOLD = '\033[1m'
            RESET = '\033[0m'
        except ImportError:
            RED = GREEN = YELLOW = BLUE = BOLD = RESET = ''
    else:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

def print_color(color, text):
    """Print colored text."""
    print(f"{color}{text}{Colors.RESET}")

def print_status(status, description, details=""):
    """Print a status line with color coding."""
    if status == "OK":
        print_color(Colors.GREEN, f"✓ {description}")
    elif status == "WARNING":
        print_color(Colors.YELLOW, f"⚠ {description}")
    elif status == "ERROR":
        print_color(Colors.RED, f"✗ {description}")
    else:
        print(f"  {description}")
    
    if details:
        print(f"    {details}")

def check_command(command):
    """Check if a command is available."""
    try:
        subprocess.run([command, "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_version(command, version_arg="--version"):
    """Get version of a command."""
    try:
        result = subprocess.run([command, version_arg], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def check_python_package(package):
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    """Run the environment check."""
    print_color(Colors.BOLD + Colors.BLUE, "=" * 60)
    print_color(Colors.BOLD + Colors.BLUE, "Interactive Modular Agent Router - Environment Check")
    print_color(Colors.BOLD + Colors.BLUE, "=" * 60)
    print()

    # Check Python
    print_color(Colors.BOLD, "🐍 Python Environment:")
    python_version = get_version(sys.executable)
    if python_version:
        version_parts = python_version.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        if major >= 3 and minor >= 8:
            print_status("OK", f"Python {python_version}")
        else:
            print_status("WARNING", f"Python {python_version}", 
                        "Python 3.8+ recommended")
    else:
        print_status("ERROR", "Python not found")

    # Check pip
    if check_command("pip"):
        pip_version = get_version("pip")
        print_status("OK", f"pip {pip_version}")
    else:
        print_status("ERROR", "pip not found")

    print()

    # Check Node.js ecosystem
    print_color(Colors.BOLD, "🌐 Node.js Environment:")
    if check_command("node"):
        node_version = get_version("node")
        print_status("OK", f"Node.js {node_version}")
        
        if check_command("npm"):
            npm_version = get_version("npm")
            print_status("OK", f"npm {npm_version}")
        else:
            print_status("WARNING", "npm not found")
    else:
        print_status("WARNING", "Node.js not found", 
                    "Required for Browser, Slack, and Playwright agents")

    print()

    # Check uv/uvx
    print_color(Colors.BOLD, "📦 Package Managers:")
    if check_command("uvx"):
        uvx_version = get_version("uvx")
        print_status("OK", f"uvx {uvx_version}")
    elif check_command("uv"):
        uv_version = get_version("uv")
        print_status("OK", f"uv {uv_version}")
    else:
        print_status("WARNING", "uv/uvx not found", 
                    "Required for RAG agent MCP servers")

    print()

    # Check Python dependencies
    print_color(Colors.BOLD, "📚 Python Dependencies:")
    required_packages = {
        "rich": "For colored console output",
        "anthropic": "For Anthropic LLM routing",
        "openai": "For OpenAI LLM routing (optional)",
    }

    for package, description in required_packages.items():
        if check_python_package(package):
            print_status("OK", f"{package} - {description}")
        else:
            status = "WARNING" if package == "openai" else "ERROR"
            print_status(status, f"{package} - {description}")

    print()

    # Check configuration files
    print_color(Colors.BOLD, "⚙️ Configuration:")
    
    if Path("mcp_agent.config.yaml").exists():
        print_status("OK", "Configuration file exists")
    else:
        print_status("ERROR", "mcp_agent.config.yaml not found")

    if Path("mcp_agent.secrets.yaml").exists():
        print_status("OK", "Secrets file exists")
        
        # Check for API keys
        try:
            with open("mcp_agent.secrets.yaml", "r") as f:
                secrets_content = f.read()
                if "anthropic_api_key" in secrets_content and "anthropic_api_key" not in secrets_content:
                    print_status("WARNING", "Anthropic API key needs to be configured")
                else:
                    print_status("OK", "Anthropic API key configured")
        except Exception:
            print_status("WARNING", "Could not read secrets file")
    else:
        if Path("mcp_agent.secrets.yaml.example").exists():
            print_status("WARNING", "Secrets file not created", 
                        "Run setup script or copy from .example file")
        else:
            print_status("ERROR", "No secrets configuration found")

    print()

    # Check MCP servers (basic check)
    print_color(Colors.BOLD, "🔧 MCP Servers:")
    
    # Node.js MCP servers
    node_servers = [
        "@modelcontextprotocol/server-filesystem",
        "@modelcontextprotocol/server-puppeteer", 
        "@modelcontextprotocol/server-slack",
        "@playwright/mcp"
    ]
    
    if check_command("npm"):
        for server in node_servers:
            try:
                result = subprocess.run(["npm", "list", "-g", server], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print_status("OK", f"Node.js: {server}")
                else:
                    print_status("WARNING", f"Node.js: {server} not installed")
            except:
                print_status("WARNING", f"Node.js: Could not check {server}")
    else:
        print_status("WARNING", "Cannot check Node.js MCP servers (npm not available)")

    print()

    # Overall assessment
    print_color(Colors.BOLD, "📋 Summary:")
    
    # Determine what agents will work
    agents_status = []
    
    # Basic routing always works with Python + Anthropic key
    if check_python_package("anthropic"):
        agents_status.append(("Basic LLM routing", "OK"))
    else:
        agents_status.append(("Basic LLM routing", "ERROR"))
    
    # Agent-specific checks
    if check_command("node") and check_command("npm"):
        agents_status.append(("Browser Agent", "OK"))
        agents_status.append(("Playwright Agent", "OK"))
        agents_status.append(("Slack Agent", "OK"))
    else:
        agents_status.append(("Browser Agent", "WARNING"))
        agents_status.append(("Playwright Agent", "WARNING"))  
        agents_status.append(("Slack Agent", "WARNING"))
    
    if check_command("uvx") or check_command("uv"):
        agents_status.append(("RAG Agent", "OK"))
    else:
        agents_status.append(("RAG Agent", "WARNING"))

    for agent, status in agents_status:
        print_status(status, agent)

    print()
    
    # Final recommendations
    errors = sum(1 for _, status in agents_status if status == "ERROR")
    warnings = sum(1 for _, status in agents_status if status == "WARNING")
    
    if errors == 0 and warnings == 0:
        print_color(Colors.GREEN, "🎉 All systems ready! You can run the full application.")
    elif errors == 0:
        print_color(Colors.YELLOW, f"⚠️  Setup mostly complete with {warnings} warnings.")
        print("   Some agents may have limited functionality.")
    else:
        print_color(Colors.RED, f"❌ Setup incomplete. {errors} errors need to be resolved.")
        
    print()
    print_color(Colors.BLUE, "💡 To install missing dependencies, run:")
    print(f"   Windows: run.bat")
    print(f"   Unix/Linux/Mac: ./run.sh")

if __name__ == "__main__":
    main()