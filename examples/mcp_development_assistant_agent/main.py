import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.swarm.swarm_anthropic import SwarmAnthropic
from mcp_agent.workflows.router.router_llm_anthropic import RouterLLMAnthropic

async def basic_dev_assistant():
    """Basic development assistant workflow"""
    app = MCPApp()
    
    # Create development assistant
    dev_assistant = Agent(
        name="DevAssistant",
        instructions="""
        You are an expert software engineer and development assistant. Your tasks include:
        1. Review code for bugs, security issues, and best practices
        2. Generate comprehensive tests for new features
        3. Create clear documentation and comments
        4. Suggest architectural improvements
        5. Automate development workflows
        6. Manage GitHub issues and pull requests
        """,
        app=app
    )
    
    # Perform code review
    result = await dev_assistant.run(
        "Review the latest pull request in the repository. "
        "Check for code quality, security issues, test coverage, and documentation. "
        "Provide specific feedback and suggestions for improvement."
    )
    
    print(result)

async def development_team():
    """Advanced Swarm pattern for team coordination"""
    app = MCPApp()
    
    # Create specialized development agents
    code_reviewer = Agent(
        name="CodeReviewer",
        instructions="""
        Expert at code review focusing on:
        - Code quality and maintainability
        - Security vulnerabilities
        - Performance optimizations
        - Best practices adherence
        """,
        app=app
    )
    
    test_engineer = Agent(
        name="TestEngineer", 
        instructions="""
        Specialist in testing strategies:
        - Unit test generation
        - Integration test design
        - Test coverage analysis
        - Testing best practices
        """,
        app=app
    )
    
    tech_writer = Agent(
        name="TechWriter",
        instructions="""
        Technical documentation expert:
        - API documentation
        - User guides and tutorials
        - Code comments and docstrings
        - Architecture documentation
        """,
        app=app
    )
    
    project_manager = Agent(
        name="ProjectManager",
        instructions="""
        Development workflow coordinator:
        - Issue triage and prioritization
        - Sprint planning assistance
        - Progress tracking
        - Team communication
        """,
        app=app
    )
    
    # Create swarm for coordinated development
    swarm = SwarmAnthropic(
        app=app,
        agents=[code_reviewer, test_engineer, tech_writer, project_manager],
        instructions="Coordinate development tasks across the team"
    )
    
    result = await swarm.run(
        "We have a new feature branch 'user-authentication' ready for review. "
        "Please coordinate the full development lifecycle: "
        "code review, test generation, documentation, and project management updates."
    )
    
    return result

async def automated_dev_workflow():
    """Automated workflow with Router pattern"""
    app = MCPApp()
    
    # Create router for different types of development tasks
    dev_router = RouterLLMAnthropic(
        app=app,
        instructions="Route development requests to appropriate specialists",
        categories={
            "code_review": "Code review, refactoring, and quality improvement",
            "testing": "Test generation, coverage analysis, and QA",
            "documentation": "Technical writing and documentation",
            "deployment": "CI/CD, deployment, and infrastructure",
            "bug_fixing": "Bug investigation and resolution"
        },
        agents={
            "code_review": Agent(name="CodeReviewer", app=app),
            "testing": Agent(name="TestEngineer", app=app),
            "documentation": Agent(name="TechWriter", app=app),
            "deployment": Agent(name="DevOpsEngineer", app=app),
            "bug_fixing": Agent(name="BugHunter", app=app)
        }
    )
    
    # Handle various development requests
    tasks = [
        "Review the authentication module for security issues",
        "Generate tests for the new payment processing feature", 
        "Create API documentation for the user service",
        "Investigate the memory leak in the image processing pipeline"
    ]
    
    results = []
    for task in tasks:
        result = await dev_router.run(task)
        results.append(result)
    
    return results

async def main():
    """Main function to run development assistant workflows"""
    print("=== MCP Development Assistant Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Assistant, 2: Team Coordination, 3: Automated Workflow): ")
    
    if workflow == "1":
        await basic_dev_assistant()
    elif workflow == "2":
        result = await development_team()
        print(result)
    elif workflow == "3":
        results = await automated_dev_workflow()
        for i, result in enumerate(results, 1):
            print(f"Task {i} Result: {result}")
    else:
        print("Invalid choice. Running basic assistant...")
        await basic_dev_assistant()

if __name__ == "__main__":
    asyncio.run(main())