# Meeting Assistant Agent

An AI-powered meeting assistant that handles the complete meeting lifecycle from scheduling to follow-up actions. This agent helps you prepare agendas, take notes, track action items, and generate insights from your meetings.

## Features

### 🗓️ **Meeting Scheduling**
- Natural language meeting requests ("Schedule a 1-hour strategy meeting with the marketing team next Tuesday")
- Calendar integration and availability checking
- Automatic invitation sending with reminders
- Meeting room booking and video call setup

### 📋 **Agenda Preparation**
- AI-generated comprehensive agendas
- Time allocation for discussion topics
- Pre-meeting preparation checklists
- Success criteria definition
- Talking points and decision frameworks

### 📝 **Smart Note-Taking**
- Automatic transcription processing
- Structured meeting minutes generation
- Action item extraction with owners and deadlines
- Key decision and quote capture
- Summary generation for absent attendees

### 📊 **Meeting Insights**
- Pattern analysis across historical meetings
- Productivity metrics and engagement tracking
- Meeting effectiveness scoring
- Recommendations for improvement
- Trend identification and reporting

### ✅ **Action Item Management**
- Automatic action item assignment
- Deadline tracking and reminders
- Progress monitoring and follow-ups
- Integration with project management tools
- Completion rate analytics

## Prerequisites

1. **Anthropic API Key** - For Claude LLM functionality
2. **Calendar Integration** - Google Calendar or Outlook API access
3. **Email Access** - For sending meeting invitations and follow-ups
4. **Optional Integrations**:
   - Notion for document management
   - Slack for team notifications
   - Zoom/Teams for video meeting creation

## Installation

1. **Clone and navigate to the example**:
   ```bash
   cd examples/mcp_meeting_assistant_agent
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

### Schedule a Meeting
```python
# Natural language scheduling
await agent.schedule_meeting(
    "Set up a quarterly review meeting with Sarah, Mike, and the finance team for next Friday at 2 PM"
)
```

### Prepare Meeting Agenda
```python
# Generate comprehensive agenda
agenda = await agent.prepare_meeting_agenda(
    meeting_context="Q4 budget planning and resource allocation",
    attendees=["Sarah Johnson", "Mike Chen", "Finance Team"]
)
```

### Process Meeting Notes
```python
# Extract structured notes from transcript
notes = await agent.take_meeting_notes(meeting_transcript)
print(notes['action_items'])  # Extracted action items with owners
```

### Generate Meeting Insights
```python
# Analyze meeting patterns
insights = await agent.generate_meeting_insights(historical_meeting_data)
```

## Interactive Demo

Run the interactive demo to explore all features:

```bash
uv run main.py
```

The demo provides a menu-driven interface to:
1. Schedule meetings with natural language
2. Generate meeting agendas
3. Process meeting transcripts into notes
4. Analyze meeting patterns for insights

## Configuration

### Meeting Settings
- **Default Duration**: 60 minutes
- **Reminder Intervals**: 24 hours, 1 hour, 15 minutes before
- **Auto-transcription**: Enabled
- **Action Item Tracking**: Enabled

### File Organization
```
/tmp/meetings/
├── agendas/          # Meeting agendas
├── notes/            # Meeting minutes
├── recordings/       # Audio/video files
├── action_items/     # Action item tracking
└── insights/         # Analytics reports
```

## MCP Server Integrations

This agent leverages multiple MCP servers:

- **Calendar Server**: Meeting scheduling and availability
- **Filesystem Server**: Document storage and organization
- **Email Server**: Invitation and notification sending
- **Search Server**: Meeting research and preparation
- **Notion Server**: Advanced document management

## Workflow Patterns

### Meeting Lifecycle Workflow
1. **Pre-Meeting**: Schedule → Prepare Agenda → Send Invites
2. **During Meeting**: Real-time note assistance
3. **Post-Meeting**: Generate Notes → Extract Actions → Follow-up

### Multi-Agent Coordination
- **Scheduler Agent**: Handles calendar operations
- **Content Agent**: Generates agendas and summaries
- **Analytics Agent**: Provides insights and metrics
- **Communication Agent**: Manages notifications

## Advanced Features

### Meeting Analytics Dashboard
- Participation rates and engagement metrics
- Meeting cost analysis (time × hourly rates)
- Decision velocity tracking
- Action item completion rates

### Smart Scheduling
- Conflict detection and resolution
- Optimal time slot suggestions
- Travel time consideration
- Timezone coordination for global teams

### Integration Ecosystem
- **Project Management**: Jira, Asana, Trello integration
- **Communication**: Slack, Teams notifications
- **Documentation**: Confluence, Notion sync
- **CRM**: Salesforce meeting logging

## Troubleshooting

### Common Issues

1. **Calendar API Errors**
   - Verify API credentials in secrets file
   - Check calendar permissions and scopes
   - Ensure proper OAuth token refresh

2. **Meeting Transcription Issues**
   - Check audio file format compatibility
   - Verify transcription service API limits
   - Ensure proper file upload permissions

3. **Action Item Tracking**
   - Confirm project management tool integration
   - Check task creation permissions
   - Verify assignee email addresses

### Performance Tips

- Use batch operations for multiple meetings
- Cache frequently accessed calendar data
- Implement smart retry logic for API calls
- Monitor token usage and rate limits

## Contributing

This example demonstrates advanced MCP-agent patterns:
- Multi-server orchestration
- Real-time data processing
- Structured information extraction
- Cross-platform integration

Feel free to extend with additional meeting platforms or productivity tools!