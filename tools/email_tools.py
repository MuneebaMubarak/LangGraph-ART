"""LangChain tools for email operations."""

from typing import List, Dict, Optional
from langchain_core.tools import tool
from services.email_service import email_service
from models.response_models import FinalAnswer

# Global variable to store the final answer for each session
_current_final_answer: Optional[FinalAnswer] = None

@tool
def search_inbox_tool(keywords: List[str]) -> List[Dict]:
    """
    Search the inbox for emails matching the given keywords.
    
    Args:
        keywords: List of keywords to search for in email subject, content, and sender
        
    Returns:
        List of email dictionaries matching the search criteria
        
    Example:
        search_inbox_tool(["budget", "review"]) -> finds emails about budget reviews
    """
    try:
        results = email_service.search_emails(keywords=keywords)
        return [email.to_dict() for email in results]
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

@tool  
def read_email_tool(message_id: str) -> Optional[Dict]:
    """
    Read a specific email by its message ID.
    
    Args:
        message_id: The unique identifier of the email to read
        
    Returns:
        Dictionary containing the full email details, or None if not found
        
    Example:
        read_email_tool("msg_001") -> returns full email content
    """
    try:
        email = email_service.get_email_by_id(message_id)
        if email:
            return email.to_dict()
        return {"error": f"Email with ID {message_id} not found"}
    except Exception as e:
        return {"error": f"Failed to read email: {str(e)}"}

@tool
def return_final_answer_tool(answer: str, reference_message_ids: List[str]) -> Dict:
    """
    Return the final answer to the user's question with source references.
    
    Args:
        answer: The final answer to the user's question
        reference_message_ids: List of email message IDs that support the answer
        
    Returns:
        Dictionary containing the formatted final answer
        
    Example:
        return_final_answer_tool(
            "The Q4 project is on track", 
            ["msg_001"]
        )
    """
    global _current_final_answer
    
    try:
        # Parse message IDs - handle both string and list input
        if isinstance(reference_message_ids, str):
            msg_ids = [id.strip() for id in reference_message_ids.split(',')]
        else:
            msg_ids = reference_message_ids
            
        _current_final_answer = FinalAnswer(
            answer=answer,
            source_ids=msg_ids
        )
        
        return {
            "final_answer": answer,
            "sources": msg_ids,
            "status": "completed"
        }
    except Exception as e:
        return {"error": f"Failed to submit final answer: {str(e)}"}

def get_current_final_answer() -> Optional[FinalAnswer]:
    """Get the current final answer from the global state."""
    return _current_final_answer

def reset_final_answer() -> None:
    """Reset the global final answer state."""
    global _current_final_answer
    _current_final_answer = None

def get_all_tools() -> List:
    """Get all available tools for the agent."""
    return [
        search_inbox_tool,
        read_email_tool, 
        return_final_answer_tool
    ]

# Tool descriptions for the agent
TOOL_DESCRIPTIONS = {
    "search_inbox_tool": "Use this to find emails by searching for keywords in subject, content, or sender",
    "read_email_tool": "Use this to read the full content of a specific email using its message ID", 
    "return_final_answer_tool": "Use this to provide your final answer with supporting email references"
}