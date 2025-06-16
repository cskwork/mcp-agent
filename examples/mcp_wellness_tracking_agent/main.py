#!/usr/bin/env python3

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class WellnessTrackingAgent(Agent):
    """
    AI-powered wellness and health tracking agent that monitors physical activity,
    nutrition, sleep, mental health, and provides personalized health insights.
    """
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(
            app=app,
            model="claude-3-5-sonnet-latest",
            temperature=0.2
        )
    
    async def track_daily_metrics(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and analyze daily health metrics"""
        
        analysis_prompt = f"""
        Analyze daily health metrics: {health_data}
        
        Evaluate:
        1. Physical activity levels and exercise patterns
        2. Nutrition intake and dietary balance
        3. Sleep quality and duration patterns
        4. Stress levels and mental wellbeing indicators
        5. Hydration and recovery metrics
        6. Progress toward health goals
        7. Risk factors and concerning trends
        8. Positive behaviors and achievements
        
        Provide personalized insights and recommendations.
        """
        
        async with self.llm as llm:
            analysis = await llm.complete(analysis_prompt)
            
            # Generate actionable recommendations
            recommendations_prompt = f"""
            Based on this analysis: {analysis}
            
            Create personalized recommendations:
            1. Exercise adjustments and workout suggestions
            2. Dietary improvements and meal planning
            3. Sleep optimization strategies
            4. Stress management techniques
            5. Hydration and recovery protocols
            6. Goal adjustments and milestone planning
            7. Preventive health measures
            8. Lifestyle modification suggestions
            
            Make recommendations specific and actionable.
            """
            
            recommendations = await llm.complete(recommendations_prompt)
            
        return {
            "daily_analysis": analysis,
            "recommendations": recommendations,
            "tracking_date": datetime.now().date().isoformat(),
            "metrics_processed": list(health_data.keys())
        }
    
    async def create_wellness_plan(self, goals: List[str], constraints: List[str]) -> str:
        """Create a personalized wellness and fitness plan"""
        
        plan_prompt = f"""
        Create a comprehensive wellness plan:
        Goals: {', '.join(goals)}
        Constraints: {', '.join(constraints)}
        
        Design:
        1. 30/60/90-day milestone framework
        2. Exercise routine with progression
        3. Nutrition plan and meal suggestions
        4. Sleep optimization protocol
        5. Stress management and mindfulness practices
        6. Progress tracking and measurement methods
        7. Habit formation and behavior change strategies
        8. Emergency protocols and motivation techniques
        
        Make it practical and sustainable.
        """
        
        async with self.llm as llm:
            wellness_plan = await llm.complete(plan_prompt)
            
        return wellness_plan
    
    async def analyze_health_trends(self, historical_data: str) -> Dict[str, Any]:
        """Analyze long-term health trends and patterns"""
        
        trend_prompt = f"""
        Analyze health trends from historical data: {historical_data}
        
        Identify:
        1. Long-term progress and improvements
        2. Concerning patterns or declining metrics
        3. Seasonal or cyclical health patterns
        4. Correlation between different health metrics
        5. Effectiveness of interventions and changes
        6. Risk factor development and prevention
        7. Achievement of health goals and milestones
        8. Areas requiring focused attention
        
        Provide trend analysis with actionable insights.
        """
        
        async with self.llm as llm:
            trends = await llm.complete(trend_prompt)
            
            # Generate health report
            report_prompt = f"""
            Create comprehensive health report: {trends}
            
            Include:
            1. Executive summary of health status
            2. Key achievements and improvements
            3. Areas of concern requiring attention
            4. Trend visualizations and charts
            5. Comparative analysis with health standards
            6. Predictive insights and future projections
            7. Personalized action plan updates
            8. Healthcare provider recommendations
            
            Format as professional health report.
            """
            
            health_report = await llm.complete(report_prompt)
            
        return {
            "trend_analysis": trends,
            "health_report": health_report,
            "analysis_period": "long_term",
            "generated_at": datetime.now().isoformat()
        }
    
    async def run_interactive_demo(self):
        """Interactive demo of wellness tracking capabilities"""
        
        print("💪 Wellness Tracking Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\nAvailable commands:")
            print("1. Track daily health metrics")
            print("2. Create wellness plan")
            print("3. Analyze health trends")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                print("Enter health data (format: metric=value):")
                steps = input("Steps taken: ")
                sleep = input("Sleep hours: ")
                water = input("Water intake (glasses): ")
                exercise = input("Exercise minutes: ")
                
                health_data = {
                    "steps": steps,
                    "sleep_hours": sleep,
                    "water_intake": water,
                    "exercise_minutes": exercise
                }
                
                result = await self.track_daily_metrics(health_data)
                print(f"\n📊 Daily analysis:\n{result['recommendations'][:500]}...")
                
            elif choice == "2":
                goals_input = input("Health goals (comma-separated): ")
                goals = [g.strip() for g in goals_input.split(",") if g.strip()]
                constraints_input = input("Constraints (comma-separated): ")
                constraints = [c.strip() for c in constraints_input.split(",") if c.strip()]
                
                plan = await self.create_wellness_plan(goals, constraints)
                print(f"\n🎯 Wellness plan:\n{plan[:500]}...")
                
            elif choice == "3":
                historical = input("Historical health data: ")
                
                trends = await self.analyze_health_trends(historical)
                print(f"\n📈 Health trends:\n{trends['health_report'][:500]}...")
                
            elif choice == "4":
                break
                
            else:
                print("Invalid option. Please try again.")


async def main():
    async with MCPApp.create() as app:
        agent = WellnessTrackingAgent(app=app, name="wellness_tracker")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())