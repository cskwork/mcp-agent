#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class PerformanceCoachingAgent(Agent):
    """AI-powered performance coaching for productivity improvement and skill development."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.3)
    
    async def assess_performance_baseline(self, performance_data: str) -> Dict[str, Any]:
        """Assess current performance baseline and identify improvement areas"""
        
        assessment_prompt = f"""
        Assess performance baseline: {performance_data}
        
        Evaluate current state:
        1. Productivity metrics and efficiency measures
        2. Skill level assessment across key competencies
        3. Work quality and consistency evaluation
        4. Time management and organization effectiveness
        5. Stress management and resilience factors
        6. Learning agility and adaptability measures
        7. Collaboration and communication effectiveness
        8. Goal achievement and milestone progress
        
        Create comprehensive performance baseline profile.
        """
        
        async with self.llm as llm:
            baseline_assessment = await llm.complete(assessment_prompt)
            
        return {"baseline_assessment": baseline_assessment, "assessed_at": datetime.now().isoformat()}
    
    async def create_coaching_plan(self, goals: List[str], assessment_results: str) -> str:
        """Create personalized coaching and development plan"""
        
        coaching_prompt = f"""
        Create coaching plan:
        Goals: {', '.join(goals)}
        Assessment: {assessment_results}
        
        Design development plan:
        1. Specific skill development priorities
        2. Performance improvement methodologies
        3. Practice exercises and skill-building activities
        4. Feedback mechanisms and progress tracking
        5. Accountability systems and check-in schedules
        6. Resource recommendations and learning materials
        7. Challenge escalation and stretch opportunities
        8. Success celebration and motivation strategies
        
        Create actionable coaching roadmap.
        """
        
        async with self.llm as llm:
            coaching_plan = await llm.complete(coaching_prompt)
            
        return coaching_plan
    
    async def provide_performance_feedback(self, performance_updates: str) -> Dict[str, Any]:
        """Provide ongoing performance feedback and recommendations"""
        
        feedback_prompt = f"""
        Provide performance feedback: {performance_updates}
        
        Deliver constructive feedback:
        1. Specific achievement recognition and celebration
        2. Improvement area identification with solutions
        3. Pattern analysis and trend observations
        4. Behavioral modification suggestions
        5. Skill gap analysis and development recommendations
        6. Obstacle identification and resolution strategies
        7. Motivation enhancement and engagement tactics
        8. Next-level challenge and growth opportunities
        
        Provide supportive and actionable feedback.
        """
        
        async with self.llm as llm:
            performance_feedback = await llm.complete(feedback_prompt)
            
        return {"performance_feedback": performance_feedback, "feedback_date": datetime.now().isoformat()}
    
    async def run_interactive_demo(self):
        print("🏆 Performance Coaching Agent - Interactive Demo")
        print("=" * 55)
        
        while True:
            print("\n1. Assess performance baseline\n2. Create coaching plan\n3. Provide feedback\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                data = input("Performance data (metrics, achievements, challenges): ")
                result = await self.assess_performance_baseline(data)
                print(f"\n📊 Baseline assessment:\n{result['baseline_assessment'][:500]}...")
            elif choice == "2":
                goals_input = input("Development goals (comma-separated): ")
                goals = [g.strip() for g in goals_input.split(",") if g.strip()]
                assessment = input("Assessment results summary: ")
                result = await self.create_coaching_plan(goals, assessment)
                print(f"\n🎯 Coaching plan:\n{result[:500]}...")
            elif choice == "3":
                updates = input("Performance updates: ")
                result = await self.provide_performance_feedback(updates)
                print(f"\n💡 Performance feedback:\n{result['performance_feedback'][:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = PerformanceCoachingAgent(app=app, name="performance_coach")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())