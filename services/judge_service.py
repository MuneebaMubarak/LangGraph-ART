"""Service for evaluating agent responses."""

import json
from tenacity import retry, stop_after_attempt, wait_exponential
from models.email_models import Scenario
from models.response_models import CorrectnessJudgeResponse
from services.llm_service import llm_service

class JudgeService:
    """Service for evaluating agent performance."""
    
    def __init__(self):
        """Initialize the judge service."""
        self.llm_service = llm_service
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def judge_correctness(self, scenario: Scenario, ai_answer: str) -> CorrectnessJudgeResponse:
        """Evaluate if the AI's answer is correct."""
        
        system_prompt = """You are an expert evaluator assessing AI responses to email-related questions.

Your task is to determine if the AI's answer is correct and acceptable based on the reference answer.

Evaluation criteria:
1. ACCURACY: Does the AI answer contain the key factual information from the reference?
2. COMPLETENESS: Does it address all parts of the question?  
3. CONSISTENCY: Is the information consistent with the reference?
4. CLARITY: Is the answer clear and well-structured?

Be somewhat lenient - the AI doesn't need to match the reference word-for-word, but should convey the same essential information correctly.

Respond with JSON in this exact format:
{
  "reasoning": "Your detailed explanation of why you accept/reject the answer",
  "accept": true/false,
  "score": 0.0-1.0
}"""
        
        user_prompt = f"""Question: {scenario.question}

Reference Answer: {scenario.expected_answer}

AI Answer: {ai_answer}

Evaluate the AI answer and respond with JSON only."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.llm_service.complete_async(
                messages=messages,
                temperature=0.1  # Low temperature for consistent evaluation
            )
            
            # Parse JSON response
            response_data = json.loads(response)
            
            return CorrectnessJudgeResponse(
                reasoning=response_data.get("reasoning", "No reasoning provided"),
                accept=response_data.get("accept", False),
                score=response_data.get("score", 0.0)
            )
            
        except json.JSONDecodeError:
            # Fallback parsing if JSON is malformed
            accept = any(phrase in response.lower() for phrase in [
                "accept: true", "\"accept\": true", "should be accepted",
                "is correct", "accurate answer"
            ])
            
            return CorrectnessJudgeResponse(
                reasoning=response,
                accept=accept,
                score=1.0 if accept else 0.0
            )
        
        except Exception as e:
            print(f"Error in judge evaluation: {e}")
            return CorrectnessJudgeResponse(
                reasoning=f"Evaluation error: {str(e)}",
                accept=False,
                score=0.0
            )
    
    async def evaluate_multiple(self, scenarios: list, answers: list) -> list:
        """Evaluate multiple scenario-answer pairs."""
        results = []
        for scenario, answer in zip(scenarios, answers):
            if answer:  # Only evaluate if we have an answer
                result = await self.judge_correctness(scenario, answer)
                results.append(result)
            else:
                results.append(CorrectnessJudgeResponse(
                    reasoning="No answer provided",
                    accept=False,
                    score=0.0
                ))
        return results
    
    def calculate_accuracy(self, evaluations: list) -> float:
        """Calculate overall accuracy from evaluations."""
        if not evaluations:
            return 0.0
        
        correct = sum(1 for eval in evaluations if eval.accept)
        return correct / len(evaluations)

# Global judge service instance  
judge_service = JudgeService()