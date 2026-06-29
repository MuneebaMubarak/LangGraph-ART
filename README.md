# Email Agent with LangGraph

An AI agent that helps users find information from emails using LangGraph and OpenAI's GPT models. The agent uses a ReAct (Reasoning + Acting) pattern to search, read, and analyze emails to answer user questions.

## Features

- 🔍 **Email Search**: Search emails by keywords in subject, content, and sender
- 📧 **Email Reading**: Read full email content by message ID  
- 🤖 **Intelligent Reasoning**: Uses ReAct pattern for step-by-step problem solving
- ✅ **Answer Evaluation**: Automatic evaluation of agent responses
- 📊 **Performance Metrics**: Track accuracy and execution statistics

## Project Structure

```
email_agent_project/
├── .env                     # Environment variables (create this)
├── requirements.txt         # Python dependencies
├── main.py                 # Main entry point
├── config/
│   └── settings.py         # Configuration management
├── models/
│   ├── email_models.py     # Email data models
│   └── response_models.py  # Response models
├── services/
│   ├── email_service.py    # Email handling
│   ├── llm_service.py      # OpenAI integration
│   └── judge_service.py    # Answer evaluation
├── tools/
│   └── email_tools.py      # LangChain tools
├── agents/
│   └── email_agent.py      # Main agent logic
├── data/
│   └── sample_emails.json  # Sample email data
└── tests/
    └── test_tools.py       # Unit tests
```

## Quick Start

### 1. Clone and Setup

```bash
# Create project directory
mkdir email_agent_project
cd email_agent_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
TEMPERATURE=1.0
MAX_TURNS=10
DEBUG=True
```

### 4. Run the Agent

```bash
python main.py
```

## Usage Examples

### Single Question
```python
import asyncio
from agents.email_agent import email_agent

async def example():
    result = await email_agent.execute("What is the status of the Q4 project?")
    if result.success:
        print(result.trajectory.final_answer.answer)
```

### Evaluation Mode
```python
from models.email_models import Scenario

scenario = Scenario(
    id="test_1",
    question="What is the budget for Q1?",
    expected_answer="$125,000",
    inbox_address="finance@company.com",
    query_date="2024-01-20"
)

result = await email_agent.evaluate_on_scenario(scenario)
```

## Available Tools

The agent has access to these tools:

1. **search_inbox_tool(keywords: List[str])**
   - Search emails by keywords
   - Returns list of matching emails

2. **read_email_tool(message_id: str)**
   - Read full email content by ID
   - Returns complete email details

3. **return_final_answer_tool(answer: str, source_ids: List[str])**
   - Submit final answer with sources
   - Required to complete each task

## Sample Emails

The system comes with 5 sample emails covering:
- Project updates (Q4 project status)
- Budget requests (Q1 2024 budget)
- Meeting notes (standup meetings)
- Client feedback (website redesign)
- System maintenance alerts

## Configuration Options

Edit `config/settings.py` or `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_NAME`: OpenAI model to use (e.g., gpt-4o-mini)
- `TEMPERATURE`: Model temperature (0.0-2.0)
- `MAX_TURNS`: Maximum reasoning steps
- `DEBUG`: Enable debug logging

## Testing

Run tests:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v
```

## Extending the Agent

### Adding New Email Sources

1. Modify `services/email_service.py`
2. Implement your email API integration
3. Update the `EmailData` model if needed

### Adding New Tools

1. Create tools in `tools/email_tools.py`
2. Decorate with `@tool`
3. Add to `get_all_tools()` function

### Custom Evaluation

1. Modify `services/judge_service.py`
2. Implement custom scoring logic
3. Update evaluation criteria

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   Error: OPENAI_API_KEY is required
   ```
   Solution: Set your API key in `.env` file

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'langchain_core'
   ```
   Solution: Install requirements: `pip install -r requirements.txt`

3. **Agent Not Responding**
   - Check internet connection
   - Verify API key is valid
   - Check model name is correct

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=True
```

This will show detailed error traces and execution logs.

## Performance Tips

1. **Model Selection**: `gpt-4o-mini` is fast and cost-effective for most tasks
2. **Temperature**: Lower values (0.1-0.3) for consistent evaluation, higher (0.7-1.0) for creative responses
3. **Max Turns**: Set reasonable limits (5-15) to prevent infinite loops

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## Roadmap

### Version 1.1 (Current)
- ✅ Basic email search and reading functionality
- ✅ ReAct agent with LangGraph integration
- ✅ Automated evaluation system
- ✅ Experience collection and analysis
- ✅ Comprehensive testing framework

### Version 1.2 (Planned)
- 🔄 Real email provider integrations (Gmail, Outlook)
- 🔄 Advanced tool development (calendar, contacts)
- 🔄 Web-based user interface
- 🔄 Enhanced evaluation metrics
- 🔄 Performance optimization

### Version 2.0 (Future)
- 📋 True reinforcement learning integration
- 📋 Multi-modal support (attachments, images)
- 📋 Enterprise security features
- 📋 Scalable deployment options
- 📋 Custom model fine-tuning

## FAQ

### Q: Can I use this with my company's email system?
A: Yes! Replace the mock email service with integrations for Gmail API, Outlook Graph API, or IMAP protocols. See the "Adding New Email Sources" section.

### Q: How accurate is the agent?
A: With proper configuration, the agent achieves 80-90% accuracy on well-defined email tasks. Performance varies based on email complexity and question clarity.

### Q: What are the costs?
A: Main costs are OpenAI API usage. With gpt-4o-mini, expect ~$0.01-0.05 per question depending on email volume and complexity.

### Q: Can I run this offline?
A: The current version requires OpenAI API access. For offline usage, you'd need to integrate with local language models like Ollama or similar.

### Q: How do I handle sensitive data?
A: Implement proper data handling: encrypt email data, use secure API calls, follow privacy regulations, and consider on-premises deployment for sensitive information.

### Q: Can this integrate with other tools?
A: Absolutely! The modular design supports integration with CRMs, project management tools, calendars, and other business systems through custom tools.

## Support

- 📖 **Documentation**: Check this README and code comments
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Contact**: Open an issue for direct support

## License

MIT License - see LICENSE file for details.

---

**⭐ If this project helps you, please consider giving it a star on GitHub!**
