#!/usr/bin/env python3

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AugmentedLLMClaude


class DocumentType(Enum):
    PROPOSAL = "proposal"
    REPORT = "report"
    CONTRACT = "contract"
    POLICY = "policy"
    MANUAL = "manual"
    PRESENTATION = "presentation"
    MEMO = "memo"
    SPECIFICATION = "specification"


class DocumentStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class DocumentWorkflowAgent(Agent):
    """
    AI-powered document workflow management agent that handles document creation,
    review, approval, versioning, and publication workflows across teams.
    """
    
    def __init__(self, app: MCPApp, name: str):
        super().__init__(app=app, name=name)
        self.llm = AugmentedLLMClaude(
            app=app,
            model="claude-3-5-sonnet-latest",
            temperature=0.2
        )
    
    async def create_document_from_brief(self, brief: str, doc_type: DocumentType) -> Dict[str, Any]:
        """Create a document from a brief description"""
        
        template_prompt = f"""
        Create a comprehensive {doc_type.value} document based on this brief:
        
        Brief: {brief}
        
        Generate:
        1. Document structure with appropriate headings
        2. Executive summary (if applicable)
        3. Main content sections with detailed information
        4. Supporting data and evidence
        5. Conclusions and recommendations
        6. Next steps or action items
        7. Appendices (if needed)
        
        Use professional formatting and ensure logical flow.
        Include placeholders for data that needs to be researched.
        """
        
        async with self.llm as llm:
            content = await llm.complete(template_prompt)
            
            # Research and enhance content
            research_prompt = f"""
            Enhance this document with research: {content}
            
            Use web search to:
            1. Find supporting statistics and data
            2. Add relevant case studies or examples
            3. Include industry best practices
            4. Verify claims and add citations
            5. Update with current information
            
            Return the enhanced document with proper citations.
            """
            
            enhanced_content = await llm.complete(research_prompt)
            
            # Save document with metadata
            save_prompt = f"""
            Save this document: {enhanced_content}
            
            Create:
            1. Filename with timestamp and version
            2. Document metadata (type, author, created date)
            3. Version control entry
            4. Tags for searchability
            5. Folder structure organization
            
            Use filesystem MCP server to organize properly.
            """
            
            save_result = await llm.complete(save_prompt)
            
        return {
            "document_content": enhanced_content,
            "document_type": doc_type.value,
            "status": DocumentStatus.DRAFT.value,
            "save_result": save_result,
            "created_at": datetime.now().isoformat()
        }
    
    async def setup_review_workflow(self, document_path: str, reviewers: List[str], 
                                   approval_levels: List[str]) -> Dict[str, Any]:
        """Set up a document review and approval workflow"""
        
        workflow_prompt = f"""
        Create a document review workflow for: {document_path}
        Reviewers: {', '.join(reviewers)}
        Approval levels: {', '.join(approval_levels)}
        
        Set up:
        1. Review assignments with deadlines
        2. Review criteria and checklists
        3. Comment collection system
        4. Version tracking for changes
        5. Approval routing sequence
        6. Notification schedule
        7. Escalation procedures for delays
        8. Final approval confirmation
        
        Use email and calendar MCP servers for notifications.
        """
        
        async with self.llm as llm:
            workflow_setup = await llm.complete(workflow_prompt)
            
            # Create review checklist
            checklist_prompt = f"""
            Create a comprehensive review checklist for this document type.
            
            Include checks for:
            1. Content accuracy and completeness
            2. Formatting and style consistency
            3. Grammar and language quality
            4. Data validation and citations
            5. Compliance with standards/policies
            6. Legal and risk considerations
            7. Accessibility requirements
            8. Technical accuracy (if applicable)
            
            Make it actionable with yes/no questions.
            """
            
            checklist = await llm.complete(checklist_prompt)
            
        return {
            "workflow_setup": workflow_setup,
            "review_checklist": checklist,
            "reviewers": reviewers,
            "approval_levels": approval_levels,
            "created_at": datetime.now().isoformat()
        }
    
    async def process_review_feedback(self, document_path: str, 
                                    feedback_data: str) -> Dict[str, Any]:
        """Process review feedback and suggest document improvements"""
        
        analysis_prompt = f"""
        Analyze this review feedback for document: {document_path}
        
        Feedback: {feedback_data}
        
        Provide:
        1. Summary of all feedback categorized by type
        2. Priority ranking of issues (critical, major, minor)
        3. Conflicting feedback identification and resolution
        4. Specific revision recommendations
        5. Areas requiring additional research
        6. Formatting and style improvements
        7. Estimated revision time and effort
        8. Quality improvement suggestions
        
        Create actionable revision plan.
        """
        
        async with self.llm as llm:
            analysis = await llm.complete(analysis_prompt)
            
            # Generate revised version
            revision_prompt = f"""
            Based on this analysis: {analysis}
            
            Create a revised version of the document addressing:
            1. All critical and major issues
            2. Style and formatting improvements
            3. Content enhancements and additions
            4. Data updates and verification
            5. Structure improvements
            
            Track changes and maintain version history.
            Use filesystem MCP server for version management.
            """
            
            revised_document = await llm.complete(revision_prompt)
            
        return {
            "feedback_analysis": analysis,
            "revised_document": revised_document,
            "status": "revised_draft",
            "revision_timestamp": datetime.now().isoformat()
        }
    
    async def automate_document_distribution(self, document_path: str, 
                                           distribution_list: List[str],
                                           distribution_type: str) -> str:
        """Automate document distribution based on type and audience"""
        
        distribution_prompt = f"""
        Set up document distribution for: {document_path}
        Recipients: {', '.join(distribution_list)}
        Type: {distribution_type}
        
        Create distribution plan:
        1. Audience-specific versions (if needed)
        2. Access permissions and security settings
        3. Delivery method (email, portal, shared drive)
        4. Read receipts and tracking
        5. Follow-up schedule for acknowledgments
        6. Archive and retention settings
        7. Update notification system
        8. Feedback collection mechanism
        
        Use email, filesystem, and web servers as needed.
        """
        
        async with self.llm as llm:
            distribution_plan = await llm.complete(distribution_prompt)
            
        return distribution_plan
    
    async def generate_document_analytics(self, document_metrics: str) -> Dict[str, Any]:
        """Generate analytics and insights from document workflow data"""
        
        analytics_prompt = f"""
        Analyze document workflow metrics: {document_metrics}
        
        Generate insights on:
        1. Review cycle times and bottlenecks
        2. Most common feedback types and patterns
        3. Reviewer effectiveness and participation
        4. Document quality improvements over time
        5. Approval process efficiency
        6. Version control and change patterns
        7. Distribution and engagement metrics
        8. Compliance and standard adherence
        
        Provide actionable recommendations for process improvement.
        """
        
        async with self.llm as llm:
            analytics = await llm.complete(analytics_prompt)
            
            # Create visualization suggestions
            viz_prompt = f"""
            Based on these analytics: {analytics}
            
            Suggest visualizations and dashboards:
            1. Workflow timeline charts
            2. Review quality scorecards
            3. Bottleneck identification graphs
            4. Trend analysis over time
            5. Reviewer performance metrics
            6. Document lifecycle tracking
            
            Create data visualization code where appropriate.
            """
            
            visualizations = await llm.complete(viz_prompt)
            
        return {
            "analytics": analytics,
            "visualizations": visualizations,
            "generated_at": datetime.now().isoformat()
        }
    
    async def run_interactive_demo(self):
        """Interactive demo of document workflow capabilities"""
        
        print("📄 Document Workflow Agent - Interactive Demo")
        print("=" * 50)
        
        while True:
            print("\nAvailable commands:")
            print("1. Create document from brief")
            print("2. Setup review workflow")
            print("3. Process review feedback")
            print("4. Setup document distribution")
            print("5. Generate workflow analytics")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                brief = input("Document brief/requirements: ")
                print("\nDocument types:")
                for i, doc_type in enumerate(DocumentType, 1):
                    print(f"{i}. {doc_type.value}")
                type_choice = input("Select type (1-8): ").strip()
                
                try:
                    doc_type = list(DocumentType)[int(type_choice) - 1]
                    result = await self.create_document_from_brief(brief, doc_type)
                    print(f"\n📝 Document created:\n{result['document_content'][:500]}...")
                except (ValueError, IndexError):
                    print("Invalid document type selection.")
                    
            elif choice == "2":
                doc_path = input("Document path: ")
                reviewers = input("Reviewers (comma-separated): ").split(",")
                reviewers = [r.strip() for r in reviewers if r.strip()]
                approval_levels = input("Approval levels (comma-separated): ").split(",")
                approval_levels = [a.strip() for a in approval_levels if a.strip()]
                
                workflow = await self.setup_review_workflow(doc_path, reviewers, approval_levels)
                print(f"\n🔄 Review workflow setup:\n{workflow['workflow_setup']}")
                
            elif choice == "3":
                doc_path = input("Document path: ")
                feedback = input("Review feedback data: ")
                
                result = await self.process_review_feedback(doc_path, feedback)
                print(f"\n📋 Feedback analysis:\n{result['feedback_analysis']}")
                
            elif choice == "4":
                doc_path = input("Document path: ")
                recipients = input("Distribution list (comma-separated): ").split(",")
                recipients = [r.strip() for r in recipients if r.strip()]
                dist_type = input("Distribution type (internal/external/public): ")
                
                plan = await self.automate_document_distribution(doc_path, recipients, dist_type)
                print(f"\n📤 Distribution plan:\n{plan}")
                
            elif choice == "5":
                metrics = input("Document workflow metrics data: ")
                analytics = await self.generate_document_analytics(metrics)
                print(f"\n📊 Workflow analytics:\n{analytics['analytics']}")
                
            elif choice == "6":
                break
                
            else:
                print("Invalid option. Please try again.")


async def main():
    """Main function to run the document workflow agent"""
    
    async with MCPApp.create() as app:
        agent = DocumentWorkflowAgent(app=app, name="document_workflow")
        
        # Run interactive demo
        await agent.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())