import asyncio
import os
import time
from datetime import datetime

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM
from mcp_agent.workflows.router.router_llm_anthropic import AnthropicRouterLLM
from mcp_agent.workflows.evaluator_optimizer.evaluator_optimizer import EvaluatorOptimizer
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM

app = MCPApp(name="legal_document_analysis")

async def legal_document_analysis():
    """
    Legal Document Analysis Agent - Automates legal document review, contract analysis, 
    compliance checking, risk assessment, and legal research to accelerate legal workflows 
    while maintaining accuracy and regulatory compliance.
    """
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context
        
        logger.info("Legal Document Analysis Agent Starting...")
        
        # Configure filesystem access for legal documents
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        # Legal operations orchestrator
        legal_orchestrator = Agent(
            name="legal_operations_orchestrator",
            instruction="""You are the Legal Operations Orchestrator responsible for 
            managing all aspects of legal document analysis and legal workflows. Your role includes:
            
            1. Coordinating document review and analysis processes
            2. Managing contract analysis and negotiation support
            3. Overseeing compliance checking and regulatory review
            4. Directing legal research and case law analysis
            5. Ensuring quality control and risk assessment
            
            You work with specialized legal agents to provide comprehensive legal services 
            while maintaining confidentiality, accuracy, and professional standards.""",
            server_names=["fetch", "filesystem", "postgres", "legal_database"]
        )
        
        # Contract analysis and review agent
        contract_agent = Agent(
            name="contract_analyzer",
            instruction="""You are a Contract Analysis specialist responsible for:
            
            1. Reviewing and analyzing contract terms and conditions
            2. Identifying key clauses, obligations, and potential risks
            3. Extracting important dates, parties, and financial terms
            4. Flagging unusual or problematic contractual provisions
            5. Providing recommendations for contract optimization
            
            Focus on thorough analysis while maintaining legal accuracy and 
            identifying potential issues that require attorney review.""",
            server_names=["filesystem", "postgres", "nlp_tools"]
        )
        
        # Compliance and regulatory analysis agent
        compliance_agent = Agent(
            name="compliance_analyzer",
            instruction="""You manage compliance and regulatory analysis by:
            
            1. Checking documents against applicable laws and regulations
            2. Identifying compliance gaps and regulatory risks
            3. Monitoring regulatory changes and their impact
            4. Ensuring industry-specific compliance requirements
            5. Providing guidance on regulatory best practices
            
            Maintain up-to-date knowledge of regulations and focus on risk mitigation.""",
            server_names=["fetch", "legal_database", "postgres"]
        )
        
        # Legal research and case law analysis agent
        research_agent = Agent(
            name="legal_researcher",
            instruction="""You provide legal research and case law analysis:
            
            1. Conducting comprehensive legal research on specific topics
            2. Analyzing relevant case law and precedents
            3. Summarizing legal opinions and court decisions
            4. Tracking legal trends and developments
            5. Providing research memoranda and legal briefs
            
            Focus on thorough research with proper citation and analysis of legal authority.""",
            server_names=["fetch", "legal_database", "case_law_api"]
        )
        
        # Document classification and metadata extraction agent
        document_agent = Agent(
            name="document_classifier",
            instruction="""You manage document classification and metadata extraction:
            
            1. Automatically classifying legal documents by type and category
            2. Extracting key metadata and document properties
            3. Identifying document relationships and dependencies
            4. Managing version control and document lineage
            5. Ensuring proper document indexing and searchability
            
            Maintain organized document systems and accurate metadata.""",
            server_names=["filesystem", "postgres", "nlp_tools"]
        )
        
        # Risk assessment and litigation support agent
        risk_agent = Agent(
            name="risk_assessor",
            instruction="""You provide risk assessment and litigation support:
            
            1. Analyzing legal risks and potential liabilities
            2. Assessing litigation probability and potential outcomes
            3. Supporting e-discovery and document production
            4. Identifying privileged and confidential information
            5. Providing strategic recommendations for risk mitigation
            
            Focus on comprehensive risk analysis and strategic legal planning.""",
            server_names=["postgres", "litigation_tools", "filesystem"]
        )
        
        async with legal_orchestrator, contract_agent, compliance_agent, research_agent, document_agent, risk_agent:
            
            # Set up legal operations orchestrator
            orchestrator_llm = await legal_orchestrator.attach_llm(AnthropicAugmentedLLM)
            orchestrator = Orchestrator(
                name="legal_document_orchestrator",
                instruction="""You coordinate all legal document analysis operations.
                Delegate tasks to specialized legal agents and ensure comprehensive 
                legal analysis and quality control.""",
                agents=[contract_agent, compliance_agent, research_agent, document_agent, risk_agent]
            )
            
            # Daily legal document processing assessment
            logger.info("Starting legal document processing workflow...")
            
            document_type = "commercial_lease_agreement"  # This would be determined dynamically
            
            legal_analysis_query = f"""Conduct a comprehensive legal analysis of a {document_type} dated {datetime.now().strftime('%Y-%m-%d')}.
            
            Please coordinate with your specialized agents to:
            
            1. Perform thorough contract analysis and identify key terms and obligations
            2. Check compliance with applicable real estate and commercial laws
            3. Research relevant case law and legal precedents
            4. Extract and organize all document metadata and classifications
            5. Assess legal risks and potential liability exposure
            
            Provide a comprehensive legal analysis report with findings, recommendations, 
            and any red flags that require immediate attorney attention."""
            
            legal_analysis = await orchestrator.generate_str(message=legal_analysis_query)
            logger.info("Legal Document Analysis", data={"report": legal_analysis})
            
            # Parallel contract analysis across multiple document sections
            logger.info("Running parallel contract section analysis...")
            
            parallel_llm = ParallelLLM(
                agents=[contract_agent, compliance_agent, risk_agent]
            )
            
            section_analysis_queries = [
                "Analyze the payment terms, rent escalations, and financial obligations in the lease agreement",
                "Review compliance with local zoning laws and ADA accessibility requirements",
                "Assess liability allocation, insurance requirements, and indemnification clauses"
            ]
            
            section_results = await parallel_llm.generate_str(section_analysis_queries)
            
            for i, result in enumerate(section_results):
                logger.info(f"Contract Section Analysis {i+1}", data={"section": section_analysis_queries[i], "analysis": result})
            
            # Contract optimization using Evaluator-Optimizer pattern
            logger.info("Optimizing contract terms and provisions...")
            
            contract_optimizer = EvaluatorOptimizer(
                task_agent=contract_agent,
                evaluator_agent=risk_agent,
                max_iterations=3
            )
            
            optimization_query = """Optimize the contract terms for better risk management and client protection:
            
            1. Strengthen termination clauses and exit strategies
            2. Improve liability limitation and risk allocation provisions
            3. Enhance dispute resolution mechanisms
            4. Clarify force majeure and contingency provisions
            5. Optimize renewal and extension terms
            
            Provide specific language recommendations that balance client interests 
            while maintaining enforceability and fairness."""
            
            contract_optimization = await contract_optimizer.generate_str(message=optimization_query)
            logger.info("Contract Optimization", data={"recommendations": contract_optimization})
            
            # Legal research and precedent analysis
            logger.info("Conducting legal research and precedent analysis...")
            
            research_analysis = await orchestrator.generate_str(
                message="""Conduct comprehensive legal research on commercial lease disputes:
                
                1. Analyze recent court decisions affecting commercial leasing
                2. Identify key precedents for rent adjustment disputes
                3. Research trends in commercial lease litigation
                4. Review regulatory changes affecting commercial real estate
                5. Assess jurisdictional variations in lease enforcement
                
                Provide a research memorandum with case citations and practical implications."""
            )
            
            logger.info("Legal Research Analysis", data={"research": research_analysis})
            
            # Router-based legal query handling
            logger.info("Setting up intelligent legal query routing...")
            
            legal_router = AnthropicRouterLLM(
                categories=[
                    "contract_analysis",
                    "compliance_review", 
                    "legal_research",
                    "document_management",
                    "risk_assessment",
                    "general_legal"
                ],
                agents=[contract_agent, compliance_agent, research_agent, document_agent, risk_agent, legal_orchestrator]
            )
            
            # Example legal queries to route
            legal_questions = [
                "What are the key provisions I should negotiate in a software licensing agreement?",
                "How do recent privacy regulations affect our data processing agreements?",
                "Can you research the latest developments in employment law regarding remote work?",
                "What metadata should we extract from merger and acquisition documents?",
                "What are the litigation risks associated with this breach of contract scenario?"
            ]
            
            for question in legal_questions:
                routed_response = await legal_router.generate_str(message=question)
                logger.info("Legal Query Response", data={"question": question, "response": routed_response})
            
            # Due diligence document review
            logger.info("Conducting due diligence document review...")
            
            due_diligence_review = await orchestrator.generate_str(
                message="""Conduct a comprehensive due diligence review for a corporate acquisition:
                
                1. Review corporate governance documents and board resolutions
                2. Analyze material contracts and ongoing obligations
                3. Assess intellectual property portfolios and protection
                4. Examine litigation history and pending legal matters
                5. Evaluate regulatory compliance and licensing status
                6. Identify potential deal-breaking issues and red flags
                
                Provide a due diligence summary with risk ratings and recommendations."""
            )
            
            logger.info("Due Diligence Review", data={"review": due_diligence_review})
            
            # Regulatory compliance monitoring
            logger.info("Monitoring regulatory compliance requirements...")
            
            compliance_monitoring = await orchestrator.generate_str(
                message="""Monitor and assess regulatory compliance across multiple jurisdictions:
                
                1. Track recent regulatory changes affecting business operations
                2. Assess compliance with data protection and privacy laws
                3. Review industry-specific regulatory requirements
                4. Evaluate cross-border compliance considerations
                5. Identify upcoming regulatory deadlines and obligations
                6. Recommend compliance improvement measures
                
                Provide a compliance dashboard with action items and priorities."""
            )
            
            logger.info("Compliance Monitoring", data={"monitoring": compliance_monitoring})
            
            # Legal analytics and insights
            logger.info("Generating legal analytics and insights...")
            
            legal_analytics = await orchestrator.generate_str(
                message="""Generate legal analytics and insights from document analysis:
                
                1. Identify patterns in contract negotiations and terms
                2. Analyze litigation outcomes and settlement trends
                3. Assess regulatory enforcement patterns and penalties
                4. Evaluate attorney performance and efficiency metrics
                5. Benchmark contract terms against industry standards
                6. Predict potential legal risks and outcomes
                
                Provide actionable insights for legal strategy and decision-making."""
            )
            
            logger.info("Legal Analytics", data={"analytics": legal_analytics})
            
            # Generate comprehensive legal summary
            logger.info("Generating final legal analysis summary...")
            
            final_summary = await orchestrator.generate_str(
                message="""Generate a comprehensive executive summary of our legal document analysis including:
                
                1. Key findings from contract and document analysis
                2. Compliance status and regulatory risk assessment
                3. Legal research insights and precedent analysis
                4. Risk mitigation recommendations and action items
                5. Process improvements and efficiency opportunities
                6. Resource allocation and priority recommendations
                7. Next steps and follow-up requirements
                
                Format as an executive briefing for legal leadership and stakeholders."""
            )
            
            logger.info("Final Legal Analysis Summary", data={"summary": final_summary})

if __name__ == "__main__":
    start = time.time()
    asyncio.run(legal_document_analysis())
    end = time.time()
    t = end - start
    
    print(f"Legal Document Analysis completed in: {t:.2f}s")