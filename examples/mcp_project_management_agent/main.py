#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class ProjectManagementAgent(Agent):
    """AI-powered project management agent for planning, tracking, and optimization."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def create_project_plan(self, project_brief: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive project plan with timeline and resource allocation"""
        
        planning_prompt = f"""
        Create project plan for: {project_brief}
        Constraints: {constraints}
        
        Develop complete plan:
        1. Project scope and deliverable definition
        2. Work breakdown structure (WBS)
        3. Timeline with critical path analysis
        4. Resource allocation and team assignments
        5. Risk assessment and mitigation strategies
        6. Budget estimation and cost tracking
        7. Quality assurance and testing protocols
        8. Communication and reporting framework
        
        Make plan detailed and actionable.
        """
        
        async with self.llm as llm:
            project_plan = await llm.complete(planning_prompt)
            
        return {"project_plan": project_plan, "brief": project_brief, "planned_at": datetime.now().isoformat()}
    
    async def track_project_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track project progress and identify bottlenecks"""
        
        tracking_prompt = f"""
        Track project progress: {progress_data}
        
        Analyze:
        1. Task completion rates and milestone progress
        2. Schedule adherence and timeline deviations
        3. Resource utilization and team productivity
        4. Budget tracking and cost variance
        5. Quality metrics and deliverable standards
        6. Risk materialization and issue escalation
        7. Team performance and workload distribution
        8. Stakeholder satisfaction and communication
        
        Identify bottlenecks and optimization opportunities.
        """
        
        async with self.llm as llm:
            progress_analysis = await llm.complete(tracking_prompt)
            
        return {"progress_analysis": progress_analysis, "tracked_at": datetime.now().isoformat()}
    
    async def optimize_project_workflow(self, workflow_data: str, issues: List[str]) -> str:
        """Optimize project workflow based on current performance"""
        
        optimization_prompt = f"""
        Optimize project workflow:
        Current Workflow: {workflow_data}
        Issues: {', '.join(issues)}
        
        Recommend improvements:
        1. Process streamlining and automation
        2. Task dependency optimization
        3. Resource reallocation for efficiency
        4. Communication workflow enhancement
        5. Tool integration and technology upgrades
        6. Team structure and role clarification
        7. Quality control checkpoint optimization
        8. Risk management process improvement
        
        Provide specific workflow optimization strategies.
        """
        
        async with self.llm as llm:
            optimized_workflow = await llm.complete(optimization_prompt)
            
        return optimized_workflow
    
    async def run_interactive_demo(self):
        print("📋 Project Management Agent - Interactive Demo")
        print("=" * 55)
        
        while True:
            print("\n1. Create project plan\n2. Track progress\n3. Optimize workflow\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                brief = input("Project brief: ")
                timeline = input("Timeline constraint: ")
                budget = input("Budget constraint: ")
                constraints = {"timeline": timeline, "budget": budget}
                result = await self.create_project_plan(brief, constraints)
                print(f"\n📝 Project plan:\n{result['project_plan'][:500]}...")
            elif choice == "2":
                data = input("Progress data: ")
                result = await self.track_project_progress({"progress": data})
                print(f"\n📈 Progress analysis:\n{result['progress_analysis'][:500]}...")
            elif choice == "3":
                workflow = input("Current workflow: ")
                issues_input = input("Issues (comma-separated): ")
                issues = [i.strip() for i in issues_input.split(",") if i.strip()]
                result = await self.optimize_project_workflow(workflow, issues)
                print(f"\n⚡ Optimized workflow:\n{result[:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = ProjectManagementAgent(app=app, name="project_manager")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())