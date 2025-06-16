# Document Workflow Agent

An AI-powered document lifecycle management system that automates document creation, review workflows, approval processes, and distribution. Perfect for organizations that need structured document management with collaboration and compliance features.

## Features

### 📝 **Intelligent Document Creation**
- Generate documents from brief descriptions
- Smart content research and enhancement
- Template-based document generation
- Auto-formatting and structure optimization
- Citation and reference management

### 🔄 **Automated Review Workflows**
- Multi-stage review process setup
- Reviewer assignment and notifications
- Review checklist generation
- Deadline tracking and escalation
- Comment collection and consolidation

### ✅ **Approval Process Management**
- Configurable approval matrices
- Role-based approval routing
- Digital signature integration
- Compliance checkpoint enforcement
- Audit trail maintenance

### 📊 **Document Analytics & Insights**
- Review cycle time analysis
- Quality improvement tracking
- Bottleneck identification
- Reviewer performance metrics
- Process optimization recommendations

### 🗂️ **Version Control & Distribution**
- Automated version management
- Change tracking and history
- Audience-specific distribution
- Access control and permissions
- Archive and retention management

## Prerequisites

1. **Anthropic API Key** - For Claude LLM functionality
2. **Document Platform Access**:
   - Google Workspace (Docs, Drive)
   - Microsoft Office 365 (Word, SharePoint)
   - Or local filesystem for simple workflows
3. **Email Integration** - For workflow notifications
4. **Optional Integrations**:
   - Confluence for documentation
   - Slack for team notifications
   - Adobe Sign or DocuSign for e-signatures

## Installation

1. **Clone and navigate to the example**:
   ```bash
   cd examples/mcp_document_workflow_agent
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure secrets**:
   ```bash
   cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
   ```
   Then edit `mcp_agent.secrets.yaml` with your API keys.

4. **Run the agent**:
   ```bash
   uv run main.py
   ```

## Usage Examples

### Create Document from Brief
```python
# Generate a comprehensive proposal
result = await agent.create_document_from_brief(
    brief="Create a proposal for implementing AI chatbots in customer service",
    doc_type=DocumentType.PROPOSAL
)
```

### Setup Review Workflow
```python
# Configure multi-stage review process
workflow = await agent.setup_review_workflow(
    document_path="proposals/ai_chatbot_proposal.docx",
    reviewers=["sarah.johnson@company.com", "mike.chen@company.com"],
    approval_levels=["manager", "director", "vp"]
)
```

### Process Review Feedback
```python
# Analyze feedback and generate revisions
result = await agent.process_review_feedback(
    document_path="proposals/ai_chatbot_proposal.docx",
    feedback_data="Reviewer comments and suggestions"
)
```

### Automate Distribution
```python
# Setup distribution workflow
plan = await agent.automate_document_distribution(
    document_path="policies/remote_work_policy.pdf",
    distribution_list=["all-employees@company.com"],
    distribution_type="internal"
)
```

## Interactive Demo

Run the interactive demo to explore all features:

```bash
uv run main.py
```

The demo provides a menu-driven interface for:
1. Creating documents from briefs
2. Setting up review workflows
3. Processing feedback and revisions
4. Configuring distribution
5. Generating analytics

## Configuration

### Document Types Supported
- **Proposals**: Business proposals and project plans
- **Reports**: Analysis and status reports
- **Contracts**: Legal agreements and contracts
- **Policies**: Company policies and procedures
- **Manuals**: User guides and documentation
- **Presentations**: Slide decks and presentations
- **Memos**: Internal communications
- **Specifications**: Technical specifications

### Workflow Stages
```yaml
review_process:
  stages:
    - content_review    # Subject matter experts
    - technical_review  # Technical accuracy
    - legal_review     # Compliance and legal
    - final_approval   # Executive sign-off
```

### File Organization
```
/tmp/documents/
├── drafts/           # Work-in-progress documents
├── reviews/          # Documents under review
├── approved/         # Approved documents
├── published/        # Published/distributed documents
├── archived/         # Archived documents
├── templates/        # Document templates
└── analytics/        # Workflow reports
```

## MCP Server Integrations

This agent leverages multiple MCP servers for comprehensive document management:

- **Filesystem Server**: Local document storage and organization
- **Google Docs Server**: Google Workspace integration
- **Office365 Server**: Microsoft Office integration
- **Email Server**: Workflow notifications and communications
- **PDF Server**: PDF generation and manipulation
- **Git Server**: Version control and change tracking
- **Search Server**: Content research and enhancement

## Workflow Patterns

### Document Lifecycle
1. **Creation**: Brief → Research → Draft → Template Application
2. **Review**: Assignment → Collection → Analysis → Revision
3. **Approval**: Routing → Validation → Sign-off → Publication
4. **Distribution**: Audience Targeting → Delivery → Tracking
5. **Maintenance**: Updates → Re-approval → Archive

### Multi-Agent Coordination
- **Content Agent**: Document creation and research
- **Workflow Agent**: Review process management
- **Approval Agent**: Sign-off and compliance
- **Distribution Agent**: Publishing and delivery
- **Analytics Agent**: Performance monitoring

## Advanced Features

### Smart Review Assignment
- Expertise-based reviewer matching
- Workload balancing across reviewers
- Conflict of interest detection
- Skill gap identification for training

### Intelligent Content Enhancement
- Automated fact-checking and citation
- Style guide compliance checking
- Readability optimization
- Accessibility improvement suggestions

### Compliance Management
- Industry-specific requirement checking
- Regulatory compliance validation
- Policy adherence verification
- Risk assessment integration

### Integration Ecosystem
- **CRM Integration**: Salesforce, HubSpot for customer documents
- **Project Management**: Jira, Asana for project documentation
- **Legal Platforms**: Contract lifecycle management
- **Quality Systems**: ISO document management

## Document Templates

The agent supports various document templates:

```python
# Proposal Template Structure
proposal_template = {
    "executive_summary": "Brief overview and key points",
    "problem_statement": "Issue identification and impact",
    "proposed_solution": "Detailed solution approach",
    "implementation_plan": "Timeline and milestones",
    "budget_analysis": "Cost breakdown and ROI",
    "risk_assessment": "Potential risks and mitigation",
    "conclusion": "Summary and next steps"
}
```

## Analytics Dashboard

### Key Metrics Tracked
- **Cycle Time**: Draft to approval duration
- **Review Quality**: Feedback depth and accuracy
- **Approval Efficiency**: Bottleneck identification
- **Version Control**: Change frequency and patterns
- **Distribution Success**: Reach and engagement

### Performance Insights
- Most effective review combinations
- Optimal workflow configurations
- Quality improvement trends
- Resource utilization patterns

## Troubleshooting

### Common Issues

1. **Document Format Compatibility**
   - Ensure proper MCP server configuration
   - Check file format support
   - Verify API permissions

2. **Review Workflow Delays**
   - Configure appropriate reminder intervals
   - Set up escalation procedures
   - Monitor reviewer workloads

3. **Approval Process Bottlenecks**
   - Analyze approval matrix effectiveness
   - Implement parallel approval paths
   - Automate routine approvals

### Performance Optimization

- Use document templates for consistency
- Implement smart caching for frequent operations
- Batch similar operations together
- Monitor API rate limits and usage

## Contributing

This example demonstrates advanced document management patterns:
- Multi-stage workflow orchestration
- Template-based content generation
- Collaborative review processes
- Compliance and approval automation

Perfect for organizations needing structured document workflows with AI assistance!