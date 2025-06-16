import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.router.router_llm_anthropic import RouterLLMAnthropic
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

async def basic_infrastructure_monitoring():
    """Basic infrastructure monitoring workflow"""
    app = MCPApp()
    
    # Create infrastructure monitoring agent
    devops_agent = Agent(
        name="DevOpsAgent",
        instructions="""
        You are a senior DevOps engineer and site reliability expert. Your responsibilities include:
        1. Monitor infrastructure health and performance metrics
        2. Automate deployment processes and CI/CD pipelines
        3. Respond to incidents and perform troubleshooting
        4. Manage cloud resources and optimize costs
        5. Implement security best practices and compliance
        6. Plan capacity and scale infrastructure as needed
        7. Generate operational reports and documentation
        8. Coordinate with development teams on releases
        
        Always prioritize system stability and security in all operations.
        """,
        app=app
    )
    
    # Monitor and respond to infrastructure issues
    result = await devops_agent.run(
        "Check the health of our production Kubernetes cluster. "
        "Review CPU, memory, and network usage across all nodes. "
        "Identify any pods with high restart counts or error rates. "
        "Check for any pending alerts in Prometheus and suggest remediation actions."
    )
    
    print(result)

async def incident_response_system():
    """Router pattern for incident response"""
    app = MCPApp()
    
    # Create router for different types of infrastructure incidents
    incident_router = RouterLLMAnthropic(
        app=app,
        instructions="Route infrastructure incidents to appropriate response teams",
        categories={
            "performance_issues": "High CPU, memory, or network performance problems",
            "service_outages": "Application or service unavailability",
            "security_incidents": "Security breaches, vulnerabilities, or compliance issues",
            "deployment_failures": "Failed deployments, rollbacks, or CI/CD issues",
            "capacity_planning": "Resource scaling, capacity limits, and optimization"
        },
        agents={
            "performance_issues": Agent(
                name="PerformanceEngineer",
                instructions="""
                Performance optimization specialist focusing on:
                - System resource monitoring and tuning
                - Database performance optimization
                - Network latency and throughput issues
                - Application performance profiling
                """,
                app=app
            ),
            "service_outages": Agent(
                name="IncidentCommander",
                instructions="""
                Incident response coordinator focusing on:
                - Service restoration and emergency procedures
                - Root cause analysis and post-mortems
                - Communication with stakeholders
                - Escalation and team coordination
                """,
                app=app
            ),
            "security_incidents": Agent(
                name="SecurityEngineer",
                instructions="""
                Security and compliance specialist focusing on:
                - Vulnerability assessment and remediation
                - Security scanning and policy enforcement
                - Compliance monitoring and reporting
                - Incident containment and forensics
                """,
                app=app
            ),
            "deployment_failures": Agent(
                name="ReleaseEngineer",
                instructions="""
                Deployment and release specialist focusing on:
                - CI/CD pipeline troubleshooting
                - Automated testing and quality gates
                - Blue-green and canary deployments
                - Rollback procedures and version control
                """,
                app=app
            ),
            "capacity_planning": Agent(
                name="CapacityPlanner",
                instructions="""
                Infrastructure capacity specialist focusing on:
                - Resource utilization analysis
                - Auto-scaling configuration
                - Cost optimization strategies
                - Growth planning and forecasting
                """,
                app=app
            )
        }
    )
    
    # Handle various infrastructure incidents
    incidents = [
        "CPU usage on production servers spiked to 95% for the last 30 minutes",
        "Payment service is returning 500 errors for 50% of requests",
        "Security scan detected critical vulnerabilities in container images",
        "Latest deployment failed with database migration errors",
        "Storage usage is at 85% capacity across all environments"
    ]
    
    results = []
    for incident in incidents:
        result = await incident_router.run(incident)
        results.append(result)
    
    return results

async def deployment_pipeline():
    """Orchestrator pattern for deployment pipeline"""
    app = MCPApp()
    
    # Create orchestrated deployment pipeline
    deployment_orchestrator = Orchestrator(
        app=app,
        instructions="Coordinate comprehensive deployment pipeline activities",
        workers=[
            Agent(
                name="CodeAnalyzer",
                instructions="""
                Code quality and security analysis specialist:
                - Static code analysis and vulnerability scanning
                - Code coverage and test quality assessment
                - Dependency checking and license compliance
                - Performance and security best practices validation
                """,
                app=app
            ),
            Agent(
                name="TestManager",
                instructions="""
                Testing and quality assurance coordinator:
                - Unit, integration, and end-to-end test execution
                - Test environment provisioning and management
                - Performance and load testing coordination
                - Test result analysis and reporting
                """,
                app=app
            ),
            Agent(
                name="InfrastructureProvisioner",
                instructions="""
                Infrastructure and environment management specialist:
                - Cloud resource provisioning and configuration
                - Container orchestration and service mesh setup
                - Database migrations and schema updates
                - Environment consistency and configuration management
                """,
                app=app
            ),
            Agent(
                name="DeploymentManager",
                instructions="""
                Deployment execution and monitoring specialist:
                - Application deployment and rollout strategies
                - Health checks and monitoring setup
                - Traffic routing and load balancer configuration  
                - Rollback procedures and disaster recovery
                """,
                app=app
            )
        ]
    )
    
    result = await deployment_orchestrator.run(
        "Deploy version 2.1.0 of the e-commerce application to production. "
        "The deployment includes database schema changes, new microservices, "
        "and updated frontend components. Ensure zero-downtime deployment "
        "with proper monitoring and rollback capabilities."
    )
    
    return result

async def multi_environment_monitoring():
    """Parallel monitoring across environments"""
    app = MCPApp()
    
    # Create parallel monitoring across environments
    parallel_monitor = ParallelLLM(
        app=app,
        instructions="Monitor multiple environments simultaneously",
        agents=[
            Agent(
                name="ProductionMonitor",
                instructions="Monitor production environment health and performance",
                app=app
            ),
            Agent(
                name="StagingMonitor",
                instructions="Monitor staging environment and pre-production testing",
                app=app
            ),
            Agent(
                name="DevelopmentMonitor",
                instructions="Monitor development environments and CI/CD pipelines",
                app=app
            ),
            Agent(
                name="SecurityMonitor",
                instructions="Monitor security events and compliance across all environments",
                app=app
            ),
            Agent(
                name="CostMonitor",
                instructions="Monitor cloud costs and resource optimization opportunities",
                app=app
            )
        ]
    )
    
    # Monitor different aspects of infrastructure
    monitoring_tasks = [
        "Check production application performance and error rates",
        "Validate staging environment readiness for next release",
        "Monitor development CI/CD pipeline success rates",
        "Scan for security vulnerabilities and compliance issues",
        "Analyze cloud spending and identify cost optimization opportunities"
    ]
    
    results = await parallel_monitor.run(monitoring_tasks)
    return results

async def main():
    """Main function to run infrastructure DevOps workflows"""
    print("=== MCP Infrastructure DevOps Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Monitoring, 2: Incident Response, 3: Deployment Pipeline, 4: Multi-Environment Monitoring): ")
    
    if workflow == "1":
        await basic_infrastructure_monitoring()
    elif workflow == "2":
        results = await incident_response_system()
        for i, result in enumerate(results, 1):
            print(f"Incident {i} Result: {result}")
    elif workflow == "3":
        result = await deployment_pipeline()
        print(result)
    elif workflow == "4":
        results = await multi_environment_monitoring()
        for i, result in enumerate(results, 1):
            print(f"Environment {i} Result: {result}")
    else:
        print("Invalid choice. Running basic monitoring...")
        await basic_infrastructure_monitoring()

if __name__ == "__main__":
    asyncio.run(main())