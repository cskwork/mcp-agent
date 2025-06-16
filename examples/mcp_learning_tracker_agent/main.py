#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class LearningTrackerAgent(Agent):
    """AI-powered learning and skills development tracker for personalized education paths."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def create_learning_path(self, skill: str, current_level: str, target_level: str) -> Dict[str, Any]:
        """Create personalized learning path with milestones and resources"""
        
        path_prompt = f"""
        Create learning path for:
        Skill: {skill}
        Current Level: {current_level}
        Target Level: {target_level}
        
        Design comprehensive path:
        1. Skill assessment and gap analysis
        2. Learning objectives and milestones
        3. Structured curriculum with progression
        4. Resource recommendations (courses, books, projects)
        5. Practice exercises and hands-on projects
        6. Assessment methods and checkpoints
        7. Time estimates and scheduling
        8. Community and mentorship opportunities
        
        Make path actionable with clear next steps.
        """
        
        async with self.llm as llm:
            learning_path = await llm.complete(path_prompt)
            
        return {"learning_path": learning_path, "skill": skill, "created_at": datetime.now().isoformat()}
    
    async def track_progress(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track learning progress and adjust study plans"""
        
        progress_prompt = f"""
        Track learning progress: {learning_data}
        
        Analyze:
        1. Milestone completion and skill advancement
        2. Learning velocity and time investment
        3. Knowledge retention and application
        4. Difficulty areas and learning blocks
        5. Effective learning methods and resources
        6. Motivation patterns and engagement
        7. Real-world application opportunities
        8. Peer comparison and benchmarking
        
        Provide progress insights with study plan adjustments.
        """
        
        async with self.llm as llm:
            progress_analysis = await llm.complete(progress_prompt)
            
        return {"progress_analysis": progress_analysis, "tracked_at": datetime.now().isoformat()}
    
    async def recommend_resources(self, topic: str, learning_style: str) -> str:
        """Recommend learning resources based on topic and learning style"""
        
        resource_prompt = f"""
        Recommend learning resources for:
        Topic: {topic}
        Learning Style: {learning_style}
        
        Suggest diverse resources:
        1. Online courses and certifications
        2. Books and documentation
        3. Video tutorials and lectures
        4. Interactive labs and simulations
        5. Practice projects and challenges
        6. Communities and study groups
        7. Mentorship and coaching options
        8. Assessment and testing tools
        
        Prioritize by quality, relevance, and learning style fit.
        """
        
        async with self.llm as llm:
            resources = await llm.complete(resource_prompt)
            
        return resources
    
    async def run_interactive_demo(self):
        print("📚 Learning Tracker Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\n1. Create learning path\n2. Track progress\n3. Recommend resources\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                skill = input("Skill to learn: ")
                current = input("Current level: ")
                target = input("Target level: ")
                result = await self.create_learning_path(skill, current, target)
                print(f"\n🎯 Learning path:\n{result['learning_path'][:500]}...")
            elif choice == "2":
                data = input("Learning progress data: ")
                result = await self.track_progress({"progress_data": data})
                print(f"\n📈 Progress analysis:\n{result['progress_analysis'][:500]}...")
            elif choice == "3":
                topic = input("Learning topic: ")
                style = input("Learning style: ")
                result = await self.recommend_resources(topic, style)
                print(f"\n💡 Resource recommendations:\n{result[:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = LearningTrackerAgent(app=app, name="learning_tracker")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())