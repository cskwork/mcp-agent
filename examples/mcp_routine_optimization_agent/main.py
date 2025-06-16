#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class RoutineOptimizationAgent(Agent):
    """AI-powered daily routine optimization for maximum productivity and well-being."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def analyze_current_routine(self, routine_data: str) -> Dict[str, Any]:
        """Analyze current daily routine for optimization opportunities"""
        
        analysis_prompt = f"""
        Analyze daily routine: {routine_data}
        
        Evaluate:
        1. Time allocation efficiency and priority alignment
        2. Energy level matching with task complexity
        3. Transition time optimization and flow states
        4. Peak performance period utilization
        5. Recovery and break distribution adequacy
        6. Routine flexibility and adaptation capability
        7. Stress points and bottleneck identification
        8. Goal alignment and productivity metrics
        
        Identify optimization opportunities and improvements.
        """
        
        async with self.llm as llm:
            routine_analysis = await llm.complete(analysis_prompt)
            
        return {"routine_analysis": routine_analysis, "analyzed_at": datetime.now().isoformat()}
    
    async def design_optimal_routine(self, preferences: Dict[str, Any], constraints: List[str]) -> str:
        """Design personalized optimal daily routine"""
        
        design_prompt = f"""
        Design optimal routine:
        Preferences: {preferences}
        Constraints: {', '.join(constraints)}
        
        Create routine considering:
        1. Chronotype and natural energy patterns
        2. Work schedule and commitment integration
        3. Health and wellness activity inclusion
        4. Personal and family time allocation
        5. Skill development and learning time
        6. Social interaction and relationship maintenance
        7. Leisure and recovery period optimization
        8. Flexibility for unexpected events
        
        Design sustainable and personalized routine.
        """
        
        async with self.llm as llm:
            optimal_routine = await llm.complete(design_prompt)
            
        return optimal_routine
    
    async def track_routine_effectiveness(self, tracking_data: str) -> Dict[str, Any]:
        """Track routine effectiveness and suggest improvements"""
        
        effectiveness_prompt = f"""
        Track routine effectiveness: {tracking_data}
        
        Measure:
        1. Adherence rate and consistency patterns
        2. Productivity outcomes and goal achievement
        3. Energy level maintenance and fatigue patterns
        4. Stress level and well-being indicators
        5. Satisfaction and enjoyment metrics
        6. Health and fitness improvement tracking
        7. Time management and efficiency gains
        8. Life balance and fulfillment assessment
        
        Provide effectiveness score with improvement suggestions.
        """
        
        async with self.llm as llm:
            effectiveness_analysis = await llm.complete(effectiveness_prompt)
            
        return {"effectiveness_analysis": effectiveness_analysis, "tracked_at": datetime.now().isoformat()}
    
    async def run_interactive_demo(self):
        print("⏰ Routine Optimization Agent - Interactive Demo")
        print("=" * 55)
        
        while True:
            print("\n1. Analyze current routine\n2. Design optimal routine\n3. Track effectiveness\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                routine = input("Current routine description: ")
                result = await self.analyze_current_routine(routine)
                print(f"\n📊 Routine analysis:\n{result['routine_analysis'][:500]}...")
            elif choice == "2":
                wake_time = input("Preferred wake time: ")
                priorities = input("Top priorities: ")
                prefs = {"wake_time": wake_time, "priorities": priorities}
                constraints_input = input("Constraints (comma-separated): ")
                constraints = [c.strip() for c in constraints_input.split(",") if c.strip()]
                result = await self.design_optimal_routine(prefs, constraints)
                print(f"\n✨ Optimal routine:\n{result[:500]}...")
            elif choice == "3":
                tracking = input("Routine tracking data: ")
                result = await self.track_routine_effectiveness(tracking)
                print(f"\n📈 Effectiveness analysis:\n{result['effectiveness_analysis'][:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = RoutineOptimizationAgent(app=app, name="routine_optimizer")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())