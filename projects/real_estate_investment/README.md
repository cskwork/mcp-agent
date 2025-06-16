# Real Estate Investment Agent

## Overview
A comprehensive real estate investment agent that analyzes property markets, evaluates investment opportunities, tracks portfolio performance, and provides data-driven insights for real estate investment decisions.

## Features

### Core Capabilities
- **Market Analysis**: Comprehensive analysis of local and national real estate markets
- **Property Evaluation**: Automated property valuation and investment analysis
- **Portfolio Management**: Track and optimize real estate investment portfolios
- **Deal Flow**: Identify and evaluate potential investment opportunities
- **Risk Assessment**: Analyze market risks and investment scenarios
- **Financial Modeling**: ROI calculations, cash flow analysis, and projections

### Architecture
- **Orchestrator Pattern**: Central coordination of investment analysis workflows
- **Parallel Processing**: Simultaneous analysis of multiple properties and markets
- **Specialized Agents**: Dedicated agents for market research, valuation, and financial analysis

## Setup

1. Copy secrets file:
```bash
cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
```

2. Add your API keys and database connections to `mcp_agent.secrets.yaml`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database for real estate data

5. Run the agent:
```bash
uv run main.py
```

## Configuration

### MCP Servers
- **fetch**: Web data retrieval for market research
- **filesystem**: Local file system access for reports and documents
- **postgres**: Real estate database for properties, transactions, and analytics
- **mls**: Multiple Listing Service integration for property data
- **property_analytics**: Advanced property analysis and valuation
- **market_data**: Real estate market trends and economic indicators
- **mortgage_calculator**: Financing calculations and loan analysis
- **property_valuation**: Automated valuation models and comparables
- **demographics**: Population and economic demographic data
- **gis**: Geographic information systems for location analysis

### Database Schema
The agent expects a PostgreSQL database with tables for:
- Property listings and historical sales data
- Market trends and price indices
- Investment portfolio and performance tracking
- Demographic and economic indicators
- Mortgage rates and financing options
- Rental market data and cap rates

## Workflows

### Investment Analysis
1. **Market Research**: Analyze target markets and neighborhoods
2. **Property Screening**: Filter properties based on investment criteria
3. **Financial Analysis**: Calculate ROI, cash flow, and investment metrics
4. **Risk Assessment**: Evaluate market and property-specific risks
5. **Comparative Analysis**: Compare similar properties and investments
6. **Investment Recommendation**: Generate investment decision reports

### Portfolio Management
- Track investment property performance
- Monitor market value changes
- Analyze rental income and expenses
- Calculate portfolio-wide metrics
- Identify optimization opportunities
- Generate performance reports

### Market Monitoring
- Daily market trend analysis
- Price change alerts and notifications
- New listing identification and screening
- Market cycle analysis and predictions
- Economic indicator tracking
- Competitive landscape monitoring

## Key Benefits

- **Data-Driven Decisions**: Objective analysis based on comprehensive data
- **Market Timing**: Identify optimal buying and selling opportunities
- **Risk Mitigation**: Understand and quantify investment risks
- **Portfolio Optimization**: Maximize returns across property investments
- **Automation**: Reduce manual research and analysis time
- **Scalability**: Analyze multiple markets and properties simultaneously

## Integration Points

### Real Estate Platforms
- Zillow for property data and valuations
- Realtor.com for MLS listings and market data
- Redfin for property information and analytics
- LoopNet for commercial real estate
- RentSpree for rental market data
- CoStar for commercial property intelligence

### Financial Services
- Mortgage rate APIs for financing analysis
- Banking APIs for portfolio tracking
- Investment platform integration
- Tax calculation services
- Insurance quote systems
- Property management software

### Data Sources
- US Census Bureau for demographic data
- Bureau of Labor Statistics for employment data
- Federal Reserve Economic Data (FRED)
- Local government property records
- School district ratings and data
- Crime statistics and safety data

## Performance Metrics

### Investment Performance
- **ROI**: Return on investment for individual properties
- **Cap Rate**: Capitalization rate for income properties
- **Cash-on-Cash Return**: Cash flow relative to cash invested
- **IRR**: Internal rate of return for multi-year investments
- **DSCR**: Debt service coverage ratio for leveraged properties
- **Appreciation Rate**: Property value growth over time

### Market Analysis
- **Price-to-Rent Ratio**: Market valuation indicator
- **Days on Market**: Property liquidity metric
- **Inventory Levels**: Supply and demand balance
- **Price Trends**: Market direction and momentum
- **Absorption Rate**: Rate of property sales
- **Market Cycle Position**: Current phase of real estate cycle

### Portfolio Metrics
- **Total Return**: Combined income and appreciation returns
- **Diversification Score**: Geographic and property type distribution
- **Leverage Ratio**: Debt-to-equity across portfolio
- **Occupancy Rate**: Rental property utilization
- **Expense Ratio**: Operating expenses as percentage of income
- **Liquidity Index**: Ease of converting properties to cash

## Troubleshooting

### Common Issues
1. **Data Quality**: Validate property and market data accuracy
2. **API Rate Limits**: Monitor external service usage
3. **Market Volatility**: Account for rapid market changes
4. **Valuation Models**: Calibrate models for local market conditions

### Monitoring
- Set up alerts for significant market changes
- Monitor property listing updates and price changes
- Track portfolio performance against benchmarks
- Review model accuracy and prediction performance
- Monitor external data source availability

## Investment Strategies

### Buy and Hold
- Long-term appreciation analysis
- Rental income optimization
- Tax benefit maximization
- Refinancing strategies
- Property improvement ROI
- Exit strategy planning

### Fix and Flip
- Property condition assessment
- Renovation cost estimation
- After-repair value (ARV) calculation
- Timeline and project management
- Market timing for sales
- Profit margin optimization

### Commercial Real Estate
- Cap rate analysis and comparison
- Lease analysis and tenant evaluation
- Commercial market trends
- Property class and location scoring
- Development opportunity assessment
- Portfolio diversification strategies

## Risk Management

### Market Risks
- **Economic Cycles**: Recession and expansion impacts
- **Interest Rate Changes**: Financing cost variations
- **Regulatory Changes**: Zoning and tax law modifications
- **Natural Disasters**: Property damage and insurance risks
- **Demographic Shifts**: Population and income changes
- **Technology Disruption**: PropTech and market evolution

### Property-Specific Risks
- **Condition Issues**: Structural and maintenance problems
- **Location Factors**: Neighborhood decline or improvement
- **Tenant Risks**: Vacancy and credit quality
- **Environmental Hazards**: Contamination and remediation
- **Title Issues**: Legal and ownership complications
- **Liquidity Risk**: Difficulty in selling properties

## Compliance and Legal

### Regulatory Requirements
- Fair Housing Act compliance
- Securities regulations for syndications
- Tax law compliance and optimization
- Environmental regulations
- Zoning and land use restrictions
- Professional licensing requirements

### Documentation and Reporting
- Investment analysis documentation
- Due diligence checklists and reports
- Performance reporting to investors
- Tax reporting and record keeping
- Insurance documentation and claims
- Legal agreement management