#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class HabitTrackerAgent(Agent):
    """AI-powered habit formation and tracking agent for building positive routines."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def design_habit_system(self, goals: List[str], lifestyle: str) -> Dict[str, Any]:
        """Design comprehensive habit system based on goals and lifestyle"""
        
        system_prompt = f"""
        Design habit system for:
        Goals: {', '.join(goals)}
        Lifestyle: {lifestyle}
        
        Create system with:
        1. Habit selection and prioritization
        2. Habit stacking and routine integration
        3. Trigger identification and environment design
        4. Reward systems and motivation loops
        5. Progress tracking and milestone celebration
        6. Obstacle anticipation and contingency plans
        7. Social accountability and support structures
        8. Gradual habit building and sustainability
        
        Make system practical and sustainable for long-term success.
        """
        
        async with self.llm as llm:
            habit_system = await llm.complete(system_prompt)
            
        return {"habit_system": habit_system, "goals": goals, "designed_at": datetime.now().isoformat()}
    
    async def track_habit_performance(self, habit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track habit performance and identify patterns"""
        
        tracking_prompt = f"""
        Analyze habit performance: {habit_data}
        
        Evaluate:
        1. Habit completion rates and consistency
        2. Streak tracking and momentum patterns
        3. Environmental factors affecting performance
        4. Time-of-day and context correlations
        5. Motivation fluctuations and energy levels
        6. Obstacle patterns and failure modes
        7. Success factors and optimal conditions
        8. Habit interference and synergies
        
        Provide insights for habit optimization.
        """
        
        async with self.llm as llm:
            performance_analysis = await llm.complete(tracking_prompt)
            
        return {"performance_analysis": performance_analysis, "analyzed_at": datetime.now().isoformat()}
    
    async def optimize_habit_routine(self, current_routine: str, challenges: List[str]) -> str:
        """Optimize existing habit routine based on challenges and feedback"""
        
        optimization_prompt = f"""
        Optimize habit routine:
        Current Routine: {current_routine}
        Challenges: {', '.join(challenges)}
        
        Suggest improvements:
        1. Routine restructuring for better flow
        2. Habit modification for easier execution
        3. Environmental changes to reduce friction
        4. Time slot optimization for energy and schedule
        5. Accountability system enhancements
        6. Reward system adjustments for motivation
        7. Backup plan creation for disruptions
        8. Progressive overload for continued growth
        
        Provide specific, actionable optimization strategies.
        """
        
        async with self.llm as llm:
            optimized_routine = await llm.complete(optimization_prompt)
            
        return optimized_routine
    
    async def run_interactive_demo(self):
        print("🔄 Habit Tracker Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\n1. Design habit system\n2. Track performance\n3. Optimize routine\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                goals_input = input("Goals (comma-separated): ")
                goals = [g.strip() for g in goals_input.split(",") if g.strip()]
                lifestyle = input("Lifestyle description: ")
                result = await self.design_habit_system(goals, lifestyle)
                print(f"\n🎯 Habit system:\n{result['habit_system'][:500]}...")
            elif choice == "2":
                data = input("Habit tracking data: ")
                result = await self.track_habit_performance({"tracking_data": data})
                print(f"\n📊 Performance analysis:\n{result['performance_analysis'][:500]}...")
            elif choice == "3":
                routine = input("Current routine: ")
                challenges_input = input("Challenges (comma-separated): ")
                challenges = [c.strip() for c in challenges_input.split(",") if c.strip()]
                result = await self.optimize_habit_routine(routine, challenges)
                print(f"\n⚡ Optimized routine:\n{result[:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = HabitTrackerAgent(app=app, name="habit_tracker")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())