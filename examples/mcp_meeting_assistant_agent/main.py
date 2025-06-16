#!/usr/bin/env python3

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class MeetingAssistantAgent(Agent):
    """
    AI-powered meeting assistant that helps with scheduling, preparation, note-taking,
    and follow-up actions. Handles meeting lifecycle from preparation to execution.
    """
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(
            app=app, 
            model="claude-3-5-sonnet-latest",
            temperature=0.1
        )
    
    async def schedule_meeting(self, meeting_request: str) -> Dict[str, Any]:
        """Schedule a meeting based on natural language request"""
        
        prompt = f"""
        You are a meeting scheduler. Analyze this meeting request and extract structured information:
        
        Request: {meeting_request}
        
        Extract and return:
        1. Meeting title
        2. Suggested duration 
        3. Meeting type (in-person, video call, phone)
        4. Priority level (high, medium, low)
        5. Required attendees
        6. Optional attendees
        7. Agenda topics
        8. Preparation requirements
        9. Suggested time preferences
        10. Meeting objectives
        
        Format as structured data that can be used to create calendar entries.
        """
        
        async with self.llm as llm:
            scheduling_info = await llm.complete(prompt)
            
            # Create calendar entry using MCP tools
            calendar_prompt = f"""
            Create a calendar entry with this information: {scheduling_info}
            
            Use the calendar MCP server to:
            1. Check availability for suggested times
            2. Create the meeting
            3. Send invitations
            4. Set reminders (24h, 1h, 15min before)
            
            Return the meeting ID and confirmation details.
            """
            
            result = await llm.complete(calendar_prompt)
            
        return {
            "scheduling_info": scheduling_info,
            "calendar_result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    async def prepare_meeting_agenda(self, meeting_context: str, attendees: List[str]) -> str:
        """Generate a comprehensive meeting agenda"""
        
        prompt = f"""
        Create a detailed meeting agenda based on this context:
        
        Context: {meeting_context}
        Attendees: {', '.join(attendees)}
        
        Generate:
        1. Meeting objectives (clear, measurable)
        2. Agenda items with time allocations
        3. Discussion topics with talking points
        4. Decision points that need resolution
        5. Action items template
        6. Pre-meeting preparation checklist
        7. Success criteria for the meeting
        8. Backup discussion topics if time permits
        
        Format as a professional agenda document.
        """
        
        async with self.llm as llm:
            agenda = await llm.complete(prompt)
            
            # Save agenda to filesystem
            save_prompt = f"""
            Save this agenda to a file: {agenda}
            
            Use the filesystem MCP server to:
            1. Create filename with meeting date/title
            2. Save as both PDF and markdown formats
            3. Create a folder structure: meetings/YYYY/MM/
            4. Generate shareable link
            """
            
            save_result = await llm.complete(save_prompt)
            
        return f"{agenda}\n\n--- File Save Result ---\n{save_result}"
    
    async def take_meeting_notes(self, meeting_audio_or_transcript: str) -> Dict[str, Any]:
        """Process meeting audio/transcript into structured notes"""
        
        prompt = f"""
        Analyze this meeting content and create comprehensive notes:
        
        Content: {meeting_audio_or_transcript}
        
        Extract and organize:
        1. Key discussion points and decisions
        2. Action items with owners and deadlines
        3. Follow-up questions and unresolved issues
        4. Important quotes and statements
        5. Next steps and timeline
        6. Parking lot items for future meetings
        7. Meeting metrics (participation, engagement)
        8. Summary for absent attendees
        
        Format as structured meeting minutes.
        """
        
        async with self.llm as llm:
            notes = await llm.complete(prompt)
            
            # Create action items and follow-ups
            followup_prompt = f"""
            Based on these meeting notes: {notes}
            
            Create:
            1. Individual action item assignments with deadlines
            2. Calendar reminders for follow-ups
            3. Next meeting scheduling if needed
            4. Stakeholder update emails
            5. Project management tool updates
            
            Use appropriate MCP servers for calendar, email, and project management.
            """
            
            followups = await llm.complete(followup_prompt)
            
        return {
            "meeting_notes": notes,
            "action_items": followups,
            "timestamp": datetime.now().isoformat()
        }
    
    async def generate_meeting_insights(self, historical_meetings: str) -> str:
        """Analyze patterns across multiple meetings for insights"""
        
        prompt = f"""
        Analyze these historical meetings for patterns and insights:
        
        Historical data: {historical_meetings}
        
        Provide analysis on:
        1. Meeting frequency and duration trends
        2. Most productive meeting types and formats
        3. Common action item completion rates
        4. Attendee engagement patterns
        5. Decision-making effectiveness
        6. Time management and agenda adherence
        7. Recurring topics and themes
        8. Recommendations for improvement
        
        Generate actionable insights for better meeting management.
        """
        
        async with self.llm as llm:
            insights = await llm.complete(prompt)
            
        return insights
    
    async def run_interactive_demo(self):
        """Interactive demo of meeting assistant capabilities"""
        
        print("🤝 Meeting Assistant Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\nAvailable commands:")
            print("1. Schedule meeting")
            print("2. Prepare agenda") 
            print("3. Take meeting notes")
            print("4. Generate insights")
            print("5. Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                request = input("Describe your meeting request: ")
                result = await self.schedule_meeting(request)
                print(f"\n📅 Meeting scheduled:\n{result['scheduling_info']}")
                
            elif choice == "2":
                context = input("Meeting context/purpose: ")
                attendees = input("Attendees (comma-separated): ").split(",")
                attendees = [a.strip() for a in attendees if a.strip()]
                agenda = await self.prepare_meeting_agenda(context, attendees)
                print(f"\n📋 Meeting agenda:\n{agenda}")
                
            elif choice == "3":
                transcript = input("Meeting transcript or key points: ")
                notes = await self.take_meeting_notes(transcript)
                print(f"\n📝 Meeting notes:\n{notes['meeting_notes']}")
                print(f"\n✅ Action items:\n{notes['action_items']}")
                
            elif choice == "4":
                history = input("Historical meeting data or patterns: ")
                insights = await self.generate_meeting_insights(history)
                print(f"\n📊 Meeting insights:\n{insights}")
                
            elif choice == "5":
                break
                
            else:
                print("Invalid option. Please try again.")


async def main():
    """Main function to run the meeting assistant agent"""
    
    async with MCPApp.create() as app:
        agent = MeetingAssistantAgent(app=app, name="meeting_assistant")
        
        # Run interactive demo
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())