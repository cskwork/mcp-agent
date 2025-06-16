import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.router.router_llm_anthropic import RouterLLMAnthropic
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

async def basic_trading_analysis():
    """Basic financial trading workflow"""
    app = MCPApp()
    
    # Create financial trading agent
    trading_agent = Agent(
        name="TradingAgent",
        instructions="""
        You are a professional financial analyst and trading specialist. Your responsibilities include:
        1. Monitor market conditions and identify trading opportunities
        2. Perform technical analysis using charts and indicators
        3. Conduct fundamental analysis of companies and sectors
        4. Execute trades based on predefined strategies and risk parameters
        5. Monitor portfolio performance and risk exposure
        6. Generate investment research and market commentary
        7. Ensure compliance with trading regulations and risk limits
        8. Provide alerts for significant market events or portfolio changes
        
        IMPORTANT: Always prioritize risk management and never exceed position limits.
        """,
        app=app
    )
    
    # Analyze market and execute strategy
    result = await trading_agent.run(
        "Analyze the current market conditions for tech stocks (AAPL, GOOGL, MSFT, NVDA). "
        "Perform technical analysis, check recent news sentiment, and recommend trading actions. "
        "Consider current portfolio allocation and risk limits before making any trades."
    )
    
    print(result)

async def multi_strategy_trading():
    """Router pattern for multi-strategy trading"""
    app = MCPApp()
    
    # Create router for different trading strategies
    strategy_router = RouterLLMAnthropic(
        app=app,
        instructions="Route market analysis to appropriate trading strategies",
        categories={
            "momentum_trading": "High-frequency momentum and trend-following strategies",
            "value_investing": "Long-term value-based investment decisions",
            "swing_trading": "Medium-term position trading based on technical patterns",
            "arbitrage": "Risk-free arbitrage and spread trading opportunities",
            "options_strategies": "Options trading and complex derivatives strategies"
        },
        agents={
            "momentum_trading": Agent(
                name="MomentumTrader",
                instructions="""
                Momentum trading specialist focusing on:
                - Short-term price movements and trends
                - High-volume breakout patterns
                - News-driven momentum plays
                - Quick entry/exit strategies
                """,
                app=app
            ),
            "value_investing": Agent(
                name="ValueInvestor",
                instructions="""
                Value investing specialist focusing on:
                - Fundamental analysis and valuation metrics
                - Long-term growth potential
                - Dividend yield and financial strength
                - Contrarian investment opportunities
                """,
                app=app
            ),
            "swing_trading": Agent(
                name="SwingTrader",
                instructions="""
                Swing trading specialist focusing on:
                - Technical chart patterns and indicators
                - Support and resistance levels
                - Multi-day to multi-week positions
                - Risk-adjusted return optimization
                """,
                app=app
            ),
            "arbitrage": Agent(
                name="ArbitrageTrader",
                instructions="""
                Arbitrage specialist focusing on:
                - Price discrepancies across markets
                - Statistical arbitrage opportunities
                - Pairs trading and market neutral strategies
                - Low-risk spread trading
                """,
                app=app
            ),
            "options_strategies": Agent(
                name="OptionsTrader",
                instructions="""
                Options trading specialist focusing on:
                - Volatility trading and Greeks analysis
                - Complex options strategies
                - Covered calls and protective puts
                - Earnings and event-driven strategies
                """,
                app=app
            )
        }
    )
    
    # Analyze different market opportunities
    market_signals = [
        "TSLA showing strong momentum after earnings beat",
        "Banking sector appears undervalued based on P/E ratios",
        "SPY forming a bullish flag pattern on daily chart", 
        "Price spread between NYSE and NASDAQ for XYZ stock",
        "High implied volatility on AAPL before product announcement"
    ]
    
    results = []
    for signal in market_signals:
        result = await strategy_router.run(signal)
        results.append(result)
    
    return results

async def portfolio_management():
    """Orchestrator pattern for portfolio management"""
    app = MCPApp()
    
    # Create orchestrated portfolio management system
    portfolio_orchestrator = Orchestrator(
        app=app,
        instructions="Coordinate comprehensive portfolio management activities",
        workers=[
            Agent(
                name="MarketAnalyst",
                instructions="""
                Market research and analysis specialist:
                - Monitor global market conditions and trends
                - Analyze economic indicators and news
                - Identify sector rotation opportunities
                - Assess market sentiment and volatility
                """,
                app=app
            ),
            Agent(
                name="RiskManager",
                instructions="""
                Portfolio risk management specialist:
                - Monitor position sizes and concentration risk
                - Calculate Value at Risk (VaR) and stress testing
                - Ensure compliance with risk limits
                - Recommend hedging strategies
                """,
                app=app
            ),
            Agent(
                name="PortfolioOptimizer",
                instructions="""
                Portfolio optimization and allocation specialist:
                - Optimize asset allocation based on risk/return
                - Rebalance portfolios to target weights
                - Implement tax-loss harvesting strategies
                - Maximize risk-adjusted returns
                """,
                app=app
            ),
            Agent(
                name="ExecutionTrader",
                instructions="""
                Trade execution and order management specialist:
                - Execute trades with optimal timing and pricing
                - Manage order flow and market impact
                - Monitor execution quality and slippage
                - Coordinate with prime brokers and exchanges
                """,
                app=app
            )
        ]
    )
    
    result = await portfolio_orchestrator.run(
        "Perform comprehensive portfolio review for Q4 2024. "
        "Current portfolio value: $5M across 50 positions. "
        "Analyze performance, rebalance allocations, manage risk exposure, "
        "and execute necessary trades to optimize for year-end."
    )
    
    return result

async def multi_asset_analysis():
    """Parallel processing for multi-asset analysis"""
    app = MCPApp()
    
    # Create parallel analysis across asset classes
    parallel_analyst = ParallelLLM(
        app=app,
        instructions="Analyze multiple asset classes simultaneously",
        agents=[
            Agent(
                name="EquityAnalyst",
                instructions="Analyze equity markets and individual stocks",
                app=app
            ),
            Agent(
                name="BondAnalyst", 
                instructions="Analyze fixed income markets and interest rates",
                app=app
            ),
            Agent(
                name="CommodityAnalyst",
                instructions="Analyze commodity markets and futures",
                app=app
            ),
            Agent(
                name="ForexAnalyst",
                instructions="Analyze foreign exchange and currency markets",
                app=app
            ),
            Agent(
                name="CryptoAnalyst",
                instructions="Analyze cryptocurrency and digital asset markets",
                app=app
            )
        ]
    )
    
    # Analyze multiple asset classes
    asset_queries = [
        "Analyze S&P 500 technical setup and sector rotation",
        "Review 10-year Treasury yield trends and Fed policy impact",
        "Assess gold and oil price movements amid geopolitical tensions",
        "Evaluate USD strength against major currency pairs",
        "Analyze Bitcoin and Ethereum correlation with risk assets"
    ]
    
    results = await parallel_analyst.run(asset_queries)
    return results

async def main():
    """Main function to run financial trading workflows"""
    print("=== MCP Financial Trading Agent ===")
    print()
    
    # Choose workflow
    workflow = input("Choose workflow (1: Basic Analysis, 2: Multi-Strategy, 3: Portfolio Management, 4: Multi-Asset Analysis): ")
    
    if workflow == "1":
        await basic_trading_analysis()
    elif workflow == "2":
        results = await multi_strategy_trading()
        for i, result in enumerate(results, 1):
            print(f"Strategy {i} Result: {result}")
    elif workflow == "3":
        result = await portfolio_management()
        print(result)
    elif workflow == "4":
        results = await multi_asset_analysis()
        for i, result in enumerate(results, 1):
            print(f"Asset Class {i} Result: {result}")
    else:
        print("Invalid choice. Running basic analysis...")
        await basic_trading_analysis()

if __name__ == "__main__":
    asyncio.run(main())