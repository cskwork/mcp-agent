@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Interactive Modular Agent Router - Windows Setup & Run Script
REM ============================================================================

echo.
echo ========================================
echo  Interactive Modular Agent Router
echo ========================================
echo.

REM Colors for output
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

REM Check if Python is installed
echo %BLUE%Checking Python installation...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Python is not installed or not in PATH%RESET%
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%Found Python %PYTHON_VERSION%%RESET%

REM Check if Node.js is installed
echo %BLUE%Checking Node.js installation...%RESET%
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%WARNING: Node.js is not installed%RESET%
    echo Some MCP servers require Node.js. Install from https://nodejs.org
    echo %YELLOW%Continuing without Node.js support...%RESET%
    set NODE_AVAILABLE=false
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo %GREEN%Found Node.js !NODE_VERSION!%RESET%
    set NODE_AVAILABLE=true
)

REM Check if uv/uvx is installed
echo %BLUE%Checking uv package manager...%RESET%
uvx --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%WARNING: uvx (uv package manager) is not installed%RESET%
    echo Some MCP servers require uvx. Install with: pip install uv
    echo %YELLOW%Continuing without uvx support...%RESET%
    set UVX_AVAILABLE=false
) else (
    echo %GREEN%Found uvx%RESET%
    set UVX_AVAILABLE=true
)

REM Create virtual environment if it doesn't exist
echo %BLUE%Setting up virtual environment...%RESET%
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo %RED%ERROR: Failed to create virtual environment%RESET%
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo %RED%ERROR: Failed to activate virtual environment%RESET%
    pause
    exit /b 1
)

REM Upgrade pip
echo %BLUE%Upgrading pip...%RESET%
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo %BLUE%Installing Python dependencies...%RESET%
if exist "requirements.txt" (
    REM Handle the local mcp-agent dependency
    echo Installing mcp-agent from local source...
    if exist "..\..\..\setup.py" (
        pip install -e ..\..\..\
    ) else if exist "..\..\..\pyproject.toml" (
        pip install -e ..\..\..\
    ) else (
        echo %YELLOW%WARNING: Local mcp-agent source not found, trying pip install...%RESET%
        pip install mcp-agent
    )
    
    REM Install other dependencies
    echo Installing additional dependencies...
    pip install anthropic openai rich
    
    if %errorlevel% neq 0 (
        echo %RED%ERROR: Failed to install Python dependencies%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%Python dependencies installed successfully%RESET%
) else (
    echo %YELLOW%No requirements.txt found, installing minimal dependencies...%RESET%
    pip install anthropic openai rich
)

REM Setup configuration files
echo %BLUE%Setting up configuration...%RESET%

REM Check if secrets file exists
if not exist "mcp_agent.secrets.yaml" (
    if exist "mcp_agent.secrets.yaml.example" (
        echo %YELLOW%Creating secrets configuration file...%RESET%
        copy "mcp_agent.secrets.yaml.example" "mcp_agent.secrets.yaml" >nul
        echo %GREEN%Created mcp_agent.secrets.yaml%RESET%
        echo.
        echo %YELLOW%IMPORTANT: Please edit mcp_agent.secrets.yaml and add your API keys:%RESET%
        echo   - Anthropic API key (required for LLM routing)
        echo   - OpenAI API key (optional, for OpenAI routing)
        echo   - Slack tokens (optional, for Slack agent)
        echo.
        choice /c YN /m "Would you like to open the secrets file now to add your API keys? (Y/N)"
        if !errorlevel! equ 1 (
            notepad "mcp_agent.secrets.yaml"
        )
    ) else (
        echo %YELLOW%No secrets template found. You may need to set up API keys manually.%RESET%
    )
)

REM Check for required API keys
echo %BLUE%Checking API key configuration...%RESET%
findstr /C:"anthropic_api_key" "mcp_agent.secrets.yaml" >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%WARNING: Anthropic API key not configured%RESET%
    echo The app requires an Anthropic API key for LLM routing.
    echo Please edit mcp_agent.secrets.yaml and add your API key.
    echo.
)

REM Install Node.js MCP servers if Node is available
if "%NODE_AVAILABLE%"=="true" (
    echo %BLUE%Installing Node.js MCP servers...%RESET%
    call npm install -g @modelcontextprotocol/server-filesystem >nul 2>&1
    call npm install -g @modelcontextprotocol/server-slack >nul 2>&1
    call npm install -g @modelcontextprotocol/server-puppeteer >nul 2>&1
    call npm install -g @playwright/mcp >nul 2>&1
    echo %GREEN%Node.js MCP servers installed%RESET%
)

REM Install Python MCP servers if uvx is available
if "%UVX_AVAILABLE%"=="true" (
    echo %BLUE%Installing Python MCP servers...%RESET%
    uvx --help >nul 2>&1
    REM Note: Actual uvx installations would happen on-demand when the app runs
    echo %GREEN%Python MCP server support ready%RESET%
)

REM Final setup check
echo.
echo %GREEN%========================================%RESET%
echo %GREEN%Setup completed successfully!%RESET%
echo %GREEN%========================================%RESET%
echo.

REM Display system status
echo %BLUE%System Status:%RESET%
echo   Python: %GREEN%✓ %PYTHON_VERSION%%RESET%
if "%NODE_AVAILABLE%"=="true" (
    echo   Node.js: %GREEN%✓ !NODE_VERSION!%RESET%
) else (
    echo   Node.js: %YELLOW%⚠ Not available%RESET%
)
if "%UVX_AVAILABLE%"=="true" (
    echo   uvx: %GREEN%✓ Available%RESET%
) else (
    echo   uvx: %YELLOW%⚠ Not available%RESET%
)

echo.
echo %BLUE%Available Agents:%RESET%
echo   • RAG Agent (requires Qdrant + uvx)
echo   • Slack Agent (requires Node.js + Slack tokens)
echo   • Browser Agent (requires Node.js)
echo   • Playwright Agent (requires Node.js)

echo.
echo %GREEN%Starting Interactive Modular Agent Router...%RESET%
echo %YELLOW%Press Ctrl+C at any time to exit%RESET%
echo.

REM Run the application
python main.py

REM Check if the app ran successfully
if %errorlevel% neq 0 (
    echo.
    echo %RED%Application exited with error code %errorlevel%%RESET%
    echo.
    echo %YELLOW%Common issues:%RESET%
    echo   • Missing API keys in mcp_agent.secrets.yaml
    echo   • Required services not running (e.g., Qdrant for RAG)
    echo   • Network connectivity issues
    echo   • Missing dependencies
    echo.
    echo %BLUE%For help, check the logs above or visit:%RESET%
    echo https://github.com/anthropics/mcp-agent
    pause
) else (
    echo.
    echo %GREEN%Application closed successfully%RESET%
)

endlocal