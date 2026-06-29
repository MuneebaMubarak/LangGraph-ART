"""Main email agent implementation."""

import uuid
import time
from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from models.email_models import Scenario
from models.response_models import AgentTrajectory, AgentExecutionResult, FinalAnswer
from services.llm_service import llm_service
from services.judge_service import judge_service
from tools.email_tools import get_all_tools, get_current_final_answer, reset_final_answer
from config.settings import settings

class EmailAgent:
    """Email assistant agent using LangGraph and ReAct pattern."""
    
    def __init__(self):
        """Initialize the email agent."""
        self.llm_service = llm_service
        self.judge_service = judge_service
        self.tools = get_all_tools()
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self) -> None:
        """Set up the LangGraph ReAct agent."""
        try:
            chat_model = self.llm_service.get_chat_model()
            self.agent = create_react_agent(chat_model, self.tools)
        except Exception as e:
            print(f"Failed to setup agent: {e}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are an AI assistant that helps users find information from emails.

Your capabilities:
1. search_inbox_tool - Search for emails using keywords
2. read_email_tool - Read full email content by message ID  
3. return_final_answer_tool - Provide final answer with source references

Instructions:
- Always search for relevant emails first using keywords from the user's question
- Read the full content of promising emails to get complete information
- Provide accurate, helpful answers based on the email content
- Always cite the message IDs you used in your final answer
- If you can't find relevant information, say so clearly
- Be concise but thorough in your responses

Example workflow:
1. User asks: "What's the status of the Q4 project?"
2. You search using keywords like ["Q4", "project", "status"]
3. You read relevant emails found
4. You provide final answer with source message IDs

Remember: Always end with return_final_answer_tool to complete the task."""
    
    async def execute(self, question: str, scenario_id: Optional[str] = None) -> AgentExecutionResult:
        """Execute the agent on a question."""
        start_time = time.time()
        
        # Reset global state
        reset_final_answer()
        
        try:
            # Configure agent execution
            config = {
                "configurable": {"thread_id": str(uuid.uuid4())},
                "recursion_limit": settings.MAX_TURNS,
            }
            
            # Create messages
            messages = [
                SystemMessage(content=self._get_system_prompt()),
                HumanMessage(content=question)
            ]
            
            # Execute the agent
            result = await self.agent.ainvoke(
                {"messages": messages},
                config=config
            )
            
            # Get the final answer from global state
            final_answer = get_current_final_answer()
            
            # Create trajectory
            trajectory = AgentTrajectory(
                scenario_id=scenario_id or str(uuid.uuid4()),
                final_answer=final_answer,
                metadata={
                    "question": question,
                    "execution_time": time.time() - start_time,
                    "model": settings.MODEL_NAME,
                    "temperature": settings.TEMPERATURE
                }
            )
            
            return AgentExecutionResult(
                success=True,
                trajectory=trajectory,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def evaluate_on_scenario(self, scenario: Scenario) -> AgentExecutionResult:
        """Execute and evaluate the agent on a specific scenario."""
        # Execute the agent
        result = await self.execute(scenario.question, scenario.id)
        
        if result.success and result.trajectory and result.trajectory.final_answer:
            # Evaluate the answer
            evaluation = await self.judge_service.judge_correctness(
                scenario, 
                result.trajectory.final_answer.answer
            )
            
            # Add evaluation metrics
            result.trajectory.add_metric("correct", evaluation.accept)
            result.trajectory.add_metric("score", evaluation.score)
            result.trajectory.add_metric("reasoning", evaluation.reasoning)
        
        return result
    
    async def run_evaluation(self, scenarios: list) -> dict:
        """Run evaluation on multiple scenarios."""
        results = []
        
        print(f"Running evaluation on {len(scenarios)} scenarios...")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\nScenario {i}/{len(scenarios)}: {scenario.id}")
            print(f"Question: {scenario.question}")
            
            result = await self.evaluate_on_scenario(scenario)
            results.append(result)
            
            if result.success and result.trajectory:
                if result.trajectory.final_answer:
                    print(f"Answer: {result.trajectory.final_answer.answer}")
                    print(f"Sources: {result.trajectory.final_answer.source_ids}")
                    
                    if "correct" in result.trajectory.metrics:
                        correct = result.trajectory.metrics["correct"]
                        print(f"Evaluation: {'✅ Correct' if correct else '❌ Incorrect'}")
                else:
                    print("No final answer provided")
            else:
                print(f"Error: {result.error}")
        
        # Calculate overall metrics
        successful_results = [r for r in results if r.success and r.trajectory]
        total_scenarios = len(scenarios)
        successful_executions = len(successful_results)
        
        evaluated_results = [
            r for r in successful_results 
            if r.trajectory.final_answer and "correct" in r.trajectory.metrics
        ]
        
        correct_answers = sum(
            1 for r in evaluated_results 
            if r.trajectory.metrics["correct"]
        )
        
        accuracy = correct_answers / len(evaluated_results) if evaluated_results else 0.0
        
        summary = {
            "total_scenarios": total_scenarios,
            "successful_executions": successful_executions,
            "evaluated_answers": len(evaluated_results),
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "execution_rate": successful_executions / total_scenarios,
            "results": results
        }
        
        print(f"\n=== Evaluation Summary ===")
        print(f"Total scenarios: {total_scenarios}")
        print(f"Successful executions: {successful_executions}/{total_scenarios} ({summary['execution_rate']:.1%})")
        print(f"Evaluated answers: {len(evaluated_results)}")
        print(f"Correct answers: {correct_answers}/{len(evaluated_results)}")
        print(f"Accuracy: {accuracy:.1%}")
        
        return summary

# Global agent instance
email_agent = EmailAgent()