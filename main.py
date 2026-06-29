"""Main entry point for the email agent."""

import asyncio
from models.email_models import Scenario
from agents.email_agent import email_agent
from config.settings import settings

# Sample scenarios for testing
SAMPLE_SCENARIOS = [
    Scenario(
        id="scenario_1",
        question="What is the status of the Q4 project?",
        expected_answer="The Q4 project is on track for the December deadline, currently 75% through development phase with testing starting next week.",
        inbox_address="team@company.com",
        query_date="2024-01-20"
    ),
    Scenario(
        id="scenario_2",
        question="What is the budget amount requested for Q1 2024?",
        expected_answer="The requested budget for Q1 2024 is $125,000, with 60% for personnel costs and 25% for infrastructure improvements.",
        inbox_address="finance@company.com", 
        query_date="2024-01-20"
    ),
    Scenario(
        id="scenario_3",
        question="When is the next standup meeting scheduled?",
        expected_answer="The next meeting is scheduled for January 24.",
        inbox_address="dev-team@company.com",
        query_date="2024-01-20"
    ),
    Scenario(
        id="scenario_4",
        question="What changes did the client request for the website redesign?",
        expected_answer="The client requested changes to the footer layout and wants to add a testimonials section on the homepage.",
        inbox_address="design-team@company.com",
        query_date="2024-01-20"
    ),
    Scenario(
        id="scenario_5",
        question="When is the scheduled system maintenance?",
        expected_answer="System maintenance is scheduled for Saturday from 2 AM to 6 AM EST.",
        inbox_address="all-staff@company.com", 
        query_date="2024-01-20"
    )
]

async def demo_single_question():
    """Demo with a single question."""
    print("=== Single Question Demo ===")
    question = "What is the status of the Q4 project?"
    print(f"Question: {question}")
    
    result = await email_agent.execute(question)
    
    if result.success and result.trajectory.final_answer:
        print(f"Answer: {result.trajectory.final_answer.answer}")
        print(f"Sources: {result.trajectory.final_answer.source_ids}")
        print(f"Execution time: {result.execution_time:.2f}s")
    else:
        print(f"Error: {result.error}")

async def demo_evaluation():
    """Demo with evaluation on sample scenarios."""
    print("\n=== Evaluation Demo ===")
    summary = await email_agent.run_evaluation(SAMPLE_SCENARIOS)
    return summary

async def interactive_mode():
    """Interactive mode for testing."""
    print("\n=== Interactive Mode ===")
    print("Ask questions about the emails. Type 'quit' to exit.")
    
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        if not question:
            continue
            
        print("Processing...")
        result = await email_agent.execute(question)
        
        if result.success and result.trajectory.final_answer:
            print(f"\nAnswer: {result.trajectory.final_answer.answer}")
            print(f"Sources: {result.trajectory.final_answer.source_ids}")
        else:
            print(f"\nError: {result.error}")

def print_available_emails():
    """Print information about available sample emails."""
    from services.email_service import email_service
    
    emails = email_service.get_all_emails()
    print(f"\n=== Available Sample Emails ({len(emails)}) ===")
    for email in emails:
        print(f"ID: {email.message_id}")
        print(f"Subject: {email.subject}")
        print(f"From: {email.sender}")
        print(f"Date: {email.timestamp}")
        print("-" * 50)

async def main():
    """Main function."""
    print("🤖 Email Agent with LangGraph")
    settings.print_config()
    
    try:
        # Verify LLM connection
        print("\n🔍 Verifying OpenAI connection...")
        from services.llm_service import llm_service
        if llm_service.validate_connection():
            print("✅ OpenAI connection successful!")
        else:
            print("❌ OpenAI connection failed!")
            return
        
        print_available_emails()
        
        # Choose demo mode
        print("\n📋 Choose a demo mode:")
        print("1. Single question demo")
        print("2. Full evaluation on sample scenarios")
        print("3. Interactive mode")
        print("4. All of the above")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice in ['1', '4']:
            await demo_single_question()
            
        if choice in ['2', '4']:
            await demo_evaluation()
            
        if choice in ['3', '4']:
            await interactive_mode()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if settings.DEBUG:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())