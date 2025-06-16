#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class BudgetTrackingAgent(Agent):
    """
    AI-powered budget tracking and financial management agent that monitors expenses,
    tracks savings goals, provides spending insights, and optimizes financial decisions.
    """
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(
            app=app,
            model="claude-3-5-sonnet-latest",
            temperature=0.1
        )
    
    async def analyze_spending_patterns(self, expense_data: str) -> Dict[str, Any]:
        """Analyze spending patterns and categorize expenses"""
        
        analysis_prompt = f"""
        Analyze spending patterns: {expense_data}
        
        Categorize and evaluate:
        1. Expense categories and spending distribution
        2. Fixed vs variable expense identification
        3. Discretionary vs necessary spending
        4. Recurring payment patterns and subscriptions
        5. Seasonal spending variations
        6. Budget category performance (over/under budget)
        7. Potential cost-saving opportunities
        8. Spending habit insights and behaviors
        
        Provide detailed financial analysis with recommendations.
        """
        
        async with self.llm as llm:
            spending_analysis = await llm.complete(analysis_prompt)
            
            # Generate budget optimization suggestions
            optimization_prompt = f"""
            Based on spending analysis: {spending_analysis}
            
            Recommend budget optimizations:
            1. Areas to reduce unnecessary spending
            2. Subscription audit and cancellation suggestions
            3. Bulk purchase opportunities for savings
            4. Timing optimization for major purchases
            5. Alternative service providers for better rates
            6. Cashback and rewards program optimization
            7. Emergency fund building strategies
            8. Investment and savings reallocation
            
            Create actionable cost reduction plan.
            """
            
            optimizations = await llm.complete(optimization_prompt)
            
        return {
            "spending_analysis": spending_analysis,
            "optimization_suggestions": optimizations,
            "analysis_date": datetime.now().isoformat()
        }
    
    async def create_budget_plan(self, income: float, goals: List[str], 
                               priorities: List[str]) -> str:
        """Create a comprehensive budget plan based on income and goals"""
        
        budget_prompt = f"""
        Create budget plan for:
        Monthly Income: ${income}
        Goals: {', '.join(goals)}
        Priorities: {', '.join(priorities)}
        
        Design comprehensive budget with:
        1. 50/30/20 rule adaptation (needs/wants/savings)
        2. Category-wise budget allocation
        3. Emergency fund building strategy
        4. Debt payoff prioritization (if applicable)
        5. Savings goal timeline and milestones
        6. Investment allocation recommendations
        7. Flexibility buffer for unexpected expenses
        8. Monthly review and adjustment framework
        
        Make budget realistic and sustainable.
        """
        
        async with self.llm as llm:
            budget_plan = await llm.complete(budget_prompt)
            
        return budget_plan
    
    async def track_savings_goals(self, savings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track progress toward savings goals and adjust strategies"""
        
        tracking_prompt = f"""
        Track savings goals progress: {savings_data}
        
        Analyze:
        1. Progress toward each savings goal
        2. Monthly savings rate and consistency
        3. Goal timeline feasibility and adjustments
        4. High-yield savings account optimization
        5. Investment vs savings allocation balance
        6. Tax-advantaged account utilization
        7. Automated savings plan effectiveness
        8. Goal prioritization and rebalancing needs
        
        Provide progress report with strategic adjustments.
        """
        
        async with self.llm as llm:
            progress_analysis = await llm.complete(tracking_prompt)
            
            # Generate goal adjustment recommendations
            adjustment_prompt = f"""
            Based on savings progress: {progress_analysis}
            
            Recommend adjustments:
            1. Goal timeline modifications for realism
            2. Savings rate increases or optimizations
            3. Investment strategy changes for growth
            4. Account type changes for better returns
            5. Automated savings plan improvements
            6. Side income opportunities for acceleration
            7. Expense reduction for increased savings
            8. Goal prioritization and sequencing updates
            
            Create actionable savings optimization plan.
            """
            
            adjustments = await llm.complete(adjustment_prompt)
            
        return {
            "progress_analysis": progress_analysis,
            "goal_adjustments": adjustments,
            "tracking_date": datetime.now().isoformat()
        }
    
    async def run_interactive_demo(self):
        """Interactive demo of budget tracking capabilities"""
        
        print("💰 Budget Tracking Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\nAvailable commands:")
            print("1. Analyze spending patterns")
            print("2. Create budget plan")
            print("3. Track savings goals")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                expenses = input("Enter expense data (description, amounts, categories): ")
                
                result = await self.analyze_spending_patterns(expenses)
                print(f"\n📊 Spending analysis:\n{result['optimization_suggestions'][:500]}...")
                
            elif choice == "2":
                income = float(input("Monthly income: $"))
                goals_input = input("Financial goals (comma-separated): ")
                goals = [g.strip() for g in goals_input.split(",") if g.strip()]
                priorities_input = input("Spending priorities (comma-separated): ")
                priorities = [p.strip() for p in priorities_input.split(",") if p.strip()]
                
                plan = await self.create_budget_plan(income, goals, priorities)
                print(f"\n💡 Budget plan:\n{plan[:500]}...")
                
            elif choice == "3":
                print("Enter savings data:")
                goal1 = input("Goal 1 (name:target:current): ")
                goal2 = input("Goal 2 (name:target:current): ")
                
                savings_data = {"goals": [goal1, goal2], "monthly_rate": ""}
                result = await self.track_savings_goals(savings_data)
                print(f"\n🎯 Savings progress:\n{result['goal_adjustments'][:500]}...")
                
            elif choice == "4":
                break


async def main():
    async with MCPApp.create() as app:
        agent = BudgetTrackingAgent(app=app, name="budget_tracker")
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())