#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class TravelPlanningAgent(Agent):
    """AI-powered travel planning agent for itinerary creation, booking optimization, and trip management."""
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(app=app, model="claude-3-5-sonnet-latest", temperature=0.2)
    
    async def create_itinerary(self, destination: str, duration: int, preferences: List[str]) -> Dict[str, Any]:
        """Create comprehensive travel itinerary with day-by-day planning"""
        
        itinerary_prompt = f"""
        Create detailed travel itinerary for:
        Destination: {destination}
        Duration: {duration} days
        Preferences: {', '.join(preferences)}
        
        Plan includes:
        1. Day-by-day activity schedule with timing
        2. Must-see attractions and hidden gems
        3. Restaurant recommendations by meal and cuisine
        4. Transportation options and logistics
        5. Accommodation suggestions by area
        6. Budget breakdown by category
        7. Cultural etiquette and local customs
        8. Emergency contacts and important phrases
        
        Make practical and engaging itinerary.
        """
        
        async with self.llm as llm:
            itinerary = await llm.complete(itinerary_prompt)
            
        return {"itinerary": itinerary, "destination": destination, "duration": duration}
    
    async def optimize_bookings(self, travel_requirements: Dict[str, Any]) -> str:
        """Find and compare best travel booking options"""
        
        booking_prompt = f"""
        Optimize travel bookings: {travel_requirements}
        
        Research and compare:
        1. Flight options with price alerts and timing
        2. Hotel deals and alternative accommodations
        3. Car rental and local transportation
        4. Activity bookings and skip-the-line tickets
        5. Travel insurance recommendations
        6. Loyalty program optimization
        7. Package deal vs individual booking analysis
        8. Cancellation policies and flexibility options
        
        Provide booking strategy with cost savings.
        """
        
        async with self.llm as llm:
            booking_optimization = await llm.complete(booking_prompt)
            
        return booking_optimization
    
    async def manage_trip_logistics(self, trip_data: str) -> Dict[str, Any]:
        """Handle trip logistics, documents, and real-time updates"""
        
        logistics_prompt = f"""
        Manage trip logistics: {trip_data}
        
        Organize:
        1. Travel document checklist and expiration tracking
        2. Packing list by climate and activities
        3. Health requirements and vaccination records
        4. Travel notifications and account security
        5. Emergency contact distribution
        6. Real-time flight and weather monitoring
        7. Local SIM card and connectivity options
        8. Currency exchange and payment methods
        
        Create comprehensive travel preparation plan.
        """
        
        async with self.llm as llm:
            logistics = await llm.complete(logistics_prompt)
            
        return {"logistics_plan": logistics, "managed_at": datetime.now().isoformat()}
    
    async def run_interactive_demo(self):
        print("✈️ Travel Planning Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\n1. Create itinerary\n2. Optimize bookings\n3. Manage logistics\n4. Exit")
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                dest = input("Destination: ")
                days = int(input("Duration (days): "))
                prefs = input("Preferences (comma-separated): ").split(",")
                result = await self.create_itinerary(dest, days, [p.strip() for p in prefs])
                print(f"\n🗺️ Itinerary:\n{result['itinerary'][:500]}...")
            elif choice == "2":
                reqs = input("Travel requirements: ")
                result = await self.optimize_bookings({"requirements": reqs})
                print(f"\n💰 Booking optimization:\n{result[:500]}...")
            elif choice == "3":
                trip_info = input("Trip information: ")
                result = await self.manage_trip_logistics(trip_info)
                print(f"\n📋 Logistics plan:\n{result['logistics_plan'][:500]}...")
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = TravelPlanningAgent(app=app, name="travel_planner")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())