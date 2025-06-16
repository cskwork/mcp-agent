#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class GoalAchievementAgent(Agent):
    """AI-powered goal setting and achievement tracking with SMART methodology and milestone management."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def create_smart_goals(self, aspirations: List[str], context: str) -> Dict[str, Any]:
        """Convert aspirations into SMART goals with detailed planning"""
        
        smart_prompt = f"""
        Convert aspirations to SMART goals:
        Aspirations: {', '.join(aspirations)}
        Context: {context}
        
        Create SMART goals framework:
        1. Specific - Clear and well-defined objectives
        2. Measurable - Quantifiable success metrics
        3. Achievable - Realistic given resources and constraints
        4. Relevant - Aligned with values and priorities
        5. Time-bound - Clear deadlines and milestones
        6. Action plan breakdown with weekly/monthly steps
        7. Success criteria and progress indicators
        8. Risk assessment and contingency planning
        
        Design comprehensive goal achievement system.
        """
        
        async with self.llm as llm:
            smart_goals = await llm.complete(smart_prompt)
            
        return {"smart_goals": smart_goals, "aspirations": aspirations, "created_at": datetime.now().isoformat()}
    
    async def track_goal_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track progress toward goals and adjust strategies"""
        
        progress_prompt = f"""
        Track goal progress: {progress_data}
        
        Analyze:
        1. Milestone completion rates and timeline adherence
        2. Obstacle identification and impact assessment
        3. Motivation levels and engagement patterns
        4. Resource utilization and efficiency
        5. Strategy effectiveness and optimization needs
        6. External factor influences and adaptations
        7. Habit formation and behavior change progress
        8. Success celebration and momentum building
        
        Provide progress insights with strategy adjustments.
        """
        
        async with self.llm as llm:
            progress_analysis = await llm.complete(progress_prompt)
            
        return {"progress_analysis": progress_analysis, "tracked_at": datetime.now().isoformat()}
    
    async def optimize_goal_strategies(self, goal_data: str, challenges: List[str]) -> str:
        """Optimize goal achievement strategies based on performance"""
        
        optimization_prompt = f"""
        Optimize goal strategies:
        Goal Data: {goal_data}
        Challenges: {', '.join(challenges)}
        
        Recommend optimizations:
        1. Strategy refinement and approach modifications
        2. Resource reallocation and efficiency improvements
        3. Timeline adjustments and milestone restructuring
        4. Support system enhancement and accountability
        5. Motivation system upgrades and reward mechanisms
        6. Skill development and capability building
        7. Environment design and trigger optimization
        8. Technology and tool integration for tracking
        
        Create enhanced goal achievement methodology.
        """
        
        async with self.llm as llm:
            strategy_optimization = await llm.complete(optimization_prompt)
            
        return strategy_optimization
    
    async def run_interactive_demo(self):
        print("🎯 Goal Achievement Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\n1. Create SMART goals\n2. Track progress\n3. Optimize strategies\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                aspirations_input = input("Aspirations (comma-separated): ")
                aspirations = [a.strip() for a in aspirations_input.split(",") if a.strip()]
                context = input("Personal context and situation: ")
                result = await self.create_smart_goals(aspirations, context)
                print(f"\n🎯 SMART goals:\n{result['smart_goals'][:500]}...")
            elif choice == "2":
                progress = input("Progress data: ")
                data = {"progress_info": progress}
                result = await self.track_goal_progress(data)
                print(f"\n📈 Progress analysis:\n{result['progress_analysis'][:500]}...")
            elif choice == "3":
                goal_info = input("Goal information: ")
                challenges_input = input("Challenges (comma-separated): ")
                challenges = [c.strip() for c in challenges_input.split(",") if c.strip()]
                result = await self.optimize_goal_strategies(goal_info, challenges)
                print(f"\n⚡ Strategy optimization:\n{result[:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = GoalAchievementAgent(app=app, name="goal_achievement")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())