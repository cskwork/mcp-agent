import asyncio
import os
import time
from datetime import datetime

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM
from mcp_agent.workflows.router.router_llm_anthropic import AnthropicRouterLLM
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM

app = MCPApp(name="medical_research_clinical")

async def medical_research_clinical():
    """
    Medical Research and Clinical Trial Agent - Accelerates medical research 
    by analyzing patient data, conducting literature reviews, matching clinical trials, 
    and ensuring regulatory compliance.
    """
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context
        
        logger.info("Medical Research and Clinical Trial Agent Starting...")
        
        # Configure filesystem access for research data
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        # Main research orchestrator
        research_orchestrator = Agent(
            name="research_orchestrator",
            instruction="""You are a Medical Research Orchestrator responsible for coordinating 
            medical research activities and clinical trials. Your role includes:
            
            1. Overseeing literature reviews and research synthesis
            2. Managing patient-trial matching and recruitment
            3. Ensuring regulatory compliance and documentation
            4. Coordinating research teams and study protocols
            5. Analyzing clinical data and generating research insights
            
            You work with specialized research agents to conduct comprehensive 
            medical research while maintaining the highest standards of ethics, 
            privacy, and regulatory compliance.""",
            server_names=["fetch", "filesystem", "postgres"]
        )
        
        # Literature review and research synthesis agent
        literature_agent = Agent(
            name="literature_researcher",
            instruction="""You are a Medical Literature Research specialist who:
            
            1. Conducts comprehensive literature searches across medical databases
            2. Synthesizes research findings and identifies knowledge gaps
            3. Performs systematic reviews and meta-analyses
            4. Tracks emerging research trends and breakthrough findings
            5. Ensures research quality and identifies potential biases
            
            Focus on evidence-based medicine and maintain high standards 
            for research quality and methodology.""",
            server_names=["fetch", "postgres"]
        )
        
        # Clinical trial matching and recruitment agent
        clinical_trial_agent = Agent(
            name="clinical_trial_coordinator",
            instruction="""You specialize in clinical trial operations including:
            
            1. Matching patients to appropriate clinical trials based on eligibility criteria
            2. Managing trial recruitment and patient screening processes
            3. Monitoring trial progress and patient safety
            4. Ensuring protocol compliance and regulatory requirements
            5. Coordinating with investigators and research sites
            
            Prioritize patient safety and maintain strict confidentiality 
            while optimizing trial enrollment and outcomes.""",
            server_names=["postgres", "filesystem"]
        )
        
        # Regulatory compliance and safety monitoring agent
        regulatory_agent = Agent(
            name="regulatory_compliance",
            instruction="""You ensure regulatory compliance and safety monitoring by:
            
            1. Monitoring FDA regulations and clinical trial guidelines
            2. Managing informed consent and ethics documentation
            3. Tracking adverse events and safety signals
            4. Ensuring data integrity and audit readiness
            5. Coordinating with IRBs and regulatory authorities
            
            Maintain the highest standards of regulatory compliance 
            and patient safety throughout all research activities.""",
            server_names=["fetch", "postgres", "filesystem"]
        )
        
        # Data analytics and biostatistics agent
        analytics_agent = Agent(
            name="research_analytics",
            instruction="""You provide advanced analytics and biostatistics support:
            
            1. Designing statistical analysis plans for clinical studies
            2. Analyzing clinical trial data and generating insights
            3. Performing survival analysis and efficacy assessments
            4. Creating visualizations and research presentations
            5. Supporting publication and regulatory submission activities
            
            Apply rigorous statistical methods and ensure reproducible research.""",
            server_names=["postgres", "filesystem"]
        )
        
        async with research_orchestrator, literature_agent, clinical_trial_agent, regulatory_agent, analytics_agent:
            
            # Set up orchestrator workflow
            orchestrator_llm = await research_orchestrator.attach_llm(AnthropicAugmentedLLM)
            orchestrator = Orchestrator(
                name="medical_research_orchestrator",
                instruction="""You coordinate all aspects of medical research and clinical trials.
                Delegate tasks to specialized agents and ensure comprehensive, 
                compliant research operations.""",
                agents=[literature_agent, clinical_trial_agent, regulatory_agent, analytics_agent]
            )
            
            # Research project initiation
            logger.info("Initiating comprehensive medical research assessment...")
            
            research_query = """We are investigating a new treatment for Type 2 diabetes. 
            Please coordinate a comprehensive research initiative including:
            
            1. Literature review of current Type 2 diabetes treatments and emerging therapies
            2. Identification of ongoing clinical trials and potential patient recruitment opportunities  
            3. Regulatory requirements for a Phase II clinical trial
            4. Statistical considerations for study design and sample size calculations
            5. Safety monitoring plan and adverse event reporting procedures
            
            Provide a detailed research plan with timelines and resource requirements."""
            
            research_plan = await orchestrator.generate_str(message=research_query)
            logger.info("Research Plan Generated", data={"plan": research_plan})
            
            # Parallel literature review across multiple domains
            logger.info("Conducting parallel literature reviews...")
            
            parallel_llm = ParallelLLM(agents=[literature_agent])
            
            literature_queries = [
                "Review recent advances in GLP-1 receptor agonists for Type 2 diabetes treatment",
                "Analyze current guidelines for diabetes management from ADA and EASD",
                "Identify emerging biomarkers for diabetes progression and treatment response",
                "Survey combination therapy approaches for Type 2 diabetes management"
            ]
            
            literature_results = await parallel_llm.generate_str(literature_queries)
            
            for i, result in enumerate(literature_results):
                logger.info(f"Literature Review {i+1}", data={"topic": literature_queries[i], "findings": result})
            
            # Clinical trial feasibility assessment
            logger.info("Assessing clinical trial feasibility...")
            
            trial_feasibility = await clinical_trial_agent.attach_llm(AnthropicAugmentedLLM)
            feasibility_assessment = await trial_feasibility.generate_str(
                message="""Assess the feasibility of conducting a Phase II clinical trial for 
                a novel Type 2 diabetes treatment. Consider:
                
                1. Patient population availability and recruitment challenges
                2. Inclusion/exclusion criteria optimization
                3. Endpoint selection and measurement considerations
                4. Site selection and investigator requirements
                5. Competitive landscape and differentiation opportunities
                
                Provide recommendations for trial design optimization."""
            )
            
            logger.info("Clinical Trial Feasibility", data={"assessment": feasibility_assessment})
            
            # Regulatory compliance review
            logger.info("Reviewing regulatory requirements...")
            
            regulatory_llm = await regulatory_agent.attach_llm(AnthropicAugmentedLLM)
            regulatory_review = await regulatory_llm.generate_str(
                message="""Review regulatory requirements for a Phase II diabetes clinical trial:
                
                1. FDA IND requirements and submission timeline
                2. IRB approval process and documentation needs
                3. Informed consent requirements and patient protection measures
                4. Good Clinical Practice (GCP) compliance requirements
                5. Data integrity and electronic records management
                6. Adverse event reporting and safety monitoring obligations
                
                Provide a regulatory compliance checklist and timeline."""
            )
            
            logger.info("Regulatory Compliance Review", data={"requirements": regulatory_review})
            
            # Statistical analysis planning
            logger.info("Developing statistical analysis plan...")
            
            analytics_llm = await analytics_agent.attach_llm(AnthropicAugmentedLLM)
            statistical_plan = await analytics_llm.generate_str(
                message="""Develop a statistical analysis plan for the Phase II diabetes trial:
                
                1. Primary and secondary endpoint definitions
                2. Sample size calculations with power analysis
                3. Randomization and stratification strategy
                4. Statistical methods for efficacy and safety analyses
                5. Interim analysis and stopping rules
                6. Missing data handling and sensitivity analyses
                
                Include considerations for regulatory submission requirements."""
            )
            
            logger.info("Statistical Analysis Plan", data={"plan": statistical_plan})
            
            # Router-based research query handling
            logger.info("Setting up intelligent research query routing...")
            
            research_router = AnthropicRouterLLM(
                categories=[
                    "literature_review",
                    "clinical_trials", 
                    "regulatory_compliance",
                    "data_analytics",
                    "general_research"
                ],
                agents=[literature_agent, clinical_trial_agent, regulatory_agent, analytics_agent, research_orchestrator]
            )
            
            # Example research queries to route
            research_questions = [
                "What are the latest FDA guidance documents for diabetes drug development?",
                "How should we calculate sample size for a superiority trial with HbA1c as primary endpoint?",
                "What are the current enrollment challenges in diabetes clinical trials?",
                "Can you review the latest meta-analyses on SGLT2 inhibitor cardiovascular outcomes?"
            ]
            
            for question in research_questions:
                routed_response = await research_router.generate_str(message=question)
                logger.info("Research Query Response", data={"question": question, "response": routed_response})
            
            # Generate comprehensive research summary
            logger.info("Generating final research summary...")
            
            final_summary = await orchestrator.generate_str(
                message="""Generate a comprehensive executive summary of our Type 2 diabetes 
                research initiative including:
                
                1. Key literature findings and research landscape
                2. Clinical trial design recommendations
                3. Regulatory pathway and timeline
                4. Statistical considerations and study power
                5. Risk assessment and mitigation strategies
                6. Resource requirements and budget considerations
                7. Next steps and action items
                
                Format as an executive briefing for research leadership."""
            )
            
            logger.info("Final Research Summary", data={"summary": final_summary})

if __name__ == "__main__":
    start = time.time()
    asyncio.run(medical_research_clinical())
    end = time.time()
    t = end - start
    
    print(f"Medical Research and Clinical Trial analysis completed in: {t:.2f}s")