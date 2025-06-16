#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class EventPlanningAgent(Agent):
    """AI-powered event planning and coordination for personal and professional events."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.3)
    
    async def create_event_plan(self, event_brief: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive event plan with timeline and logistics"""
        
        planning_prompt = f"""
        Create event plan:
        Brief: {event_brief}
        Constraints: {constraints}
        
        Develop complete plan:
        1. Event concept and theme development
        2. Venue selection and booking coordination
        3. Guest list management and invitation system
        4. Catering and menu planning with dietary requirements
        5. Entertainment and activity coordination
        6. Timeline and logistics management
        7. Budget tracking and cost optimization
        8. Contingency planning and risk management
        
        Create detailed event execution plan.
        """
        
        async with self.llm as llm:
            event_plan = await llm.complete(planning_prompt)
            
        return {"event_plan": event_plan, "brief": event_brief, "planned_at": datetime.now().isoformat()}
    
    async def coordinate_logistics(self, event_details: str) -> str:
        """Coordinate event logistics and vendor management"""
        
        coordination_prompt = f"""
        Coordinate event logistics: {event_details}
        
        Manage coordination:
        1. Vendor selection and contract management
        2. Setup and breakdown timeline coordination
        3. Staff and volunteer task assignment
        4. Equipment and supply procurement
        5. Transportation and parking arrangements
        6. Technology and AV system setup
        7. Security and safety protocol implementation
        8. Communication and coordination systems
        
        Create seamless logistics execution plan.
        """
        
        async with self.llm as llm:
            logistics_plan = await llm.complete(coordination_prompt)
            
        return logistics_plan
    
    async def manage_guest_experience(self, guest_data: str) -> Dict[str, Any]:
        """Optimize guest experience and engagement"""
        
        experience_prompt = f"""
        Optimize guest experience: {guest_data}
        
        Enhance experience through:
        1. Personalized welcome and check-in process
        2. Networking facilitation and introductions
        3. Interactive activities and engagement opportunities
        4. Dietary restriction and accessibility accommodation
        5. Real-time feedback collection and adaptation
        6. Photo and memory capture coordination
        7. Follow-up communication and thank you messages
        8. Experience evaluation and improvement tracking
        
        Create memorable and engaging guest experience.
        """
        
        async with self.llm as llm:
            experience_optimization = await llm.complete(experience_prompt)
            
        return {"experience_optimization": experience_optimization, "optimized_at": datetime.now().isoformat()}
    
    async def run_interactive_demo(self):
        print("🎉 Event Planning Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\n1. Create event plan\n2. Coordinate logistics\n3. Manage guest experience\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                brief = input("Event brief and description: ")
                budget = input("Budget constraint: ")
                date = input("Date constraint: ")
                constraints = {"budget": budget, "date": date}
                result = await self.create_event_plan(brief, constraints)
                print(f"\n📋 Event plan:\n{result['event_plan'][:500]}...")
            elif choice == "2":
                details = input("Event details: ")
                result = await self.coordinate_logistics(details)
                print(f"\n🔧 Logistics coordination:\n{result[:500]}...")
            elif choice == "3":
                guest_info = input("Guest information: ")
                result = await self.manage_guest_experience(guest_info)
                print(f"\n✨ Guest experience:\n{result['experience_optimization'][:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = EventPlanningAgent(app=app, name="event_planner")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())