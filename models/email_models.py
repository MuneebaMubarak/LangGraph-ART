"""Email-related data models."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass #A Python decorator that automatically creates common methods to avoiv repetitive codes
class EmailData:
    """Represents an email in the system."""
    message_id: str
    subject: str
    content: str
    sender: str
    recipient: str
    timestamp: str
    attachments: Optional[List[str]] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for tool responses."""
        return {
            "message_id": self.message_id,
            "subject": self.subject,
            "content": self.content,
            "sender": self.sender,
            "recipient": self.recipient,
            "timestamp": self.timestamp,
            "attachments": self.attachments or []
        }
    
    def matches_keywords(self, keywords: List[str]) -> bool:
        """Check if email matches any of the given keywords."""
        searchable_text = f"{self.subject} {self.content} {self.sender}".lower()
        return any(keyword.lower() in searchable_text for keyword in keywords)

@dataclass
class Scenario:
    """Represents a test scenario for the agent."""
    id: str
    question: str
    expected_answer: str
    inbox_address: str
    query_date: str
    difficulty: str = "medium"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "question": self.question,
            "expected_answer": self.expected_answer,
            "inbox_address": self.inbox_address,
            "query_date": self.query_date,
            "difficulty": self.difficulty
        }