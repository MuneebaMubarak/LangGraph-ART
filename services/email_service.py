"""Email service for managing email data."""

import json
from typing import List, Optional
from models.email_models import EmailData

class EmailService:
    """Service for managing email operations."""
    
    def __init__(self, data_file: str = "data/sample_emails.json"):
        """Initialize the email service with sample data."""
        self.data_file = data_file
        self._emails: List[EmailData] = []
        self.load_sample_data()
    
    def load_sample_data(self) -> None:
        """Load sample email data."""
        sample_emails = [
            EmailData(
                message_id="msg_001",
                subject="Q4 Project Update - On Track",
                content="Hi team, I'm pleased to report that our Q4 project is progressing well and remains on track for the December deadline. All major milestones have been completed on time, and we're currently 75% through the development phase. The testing phase is scheduled to begin next week.",
                sender="john.doe@company.com",
                recipient="team@company.com",
                timestamp="2024-01-15T10:30:00Z"
            ),
            EmailData(
                message_id="msg_002", 
                subject="Budget Review Request - Q1 2024",
                content="Dear Finance Team, Please review the attached budget proposal for Q1 2024. The total requested budget is $125,000, with the majority allocated to personnel costs (60%) and infrastructure improvements (25%). I need your approval by Friday to proceed with the procurement process.",
                sender="finance.manager@company.com",
                recipient="finance@company.com", 
                timestamp="2024-01-16T14:45:00Z"
            ),
            EmailData(
                message_id="msg_003",
                subject="Weekly Standup Meeting Notes - Jan 17",
                content="Meeting Summary: Discussed sprint progress, resolved 3 blocking issues, and planned next week's priorities. Action items: Sarah to review API documentation, Mike to fix authentication bug, Lisa to prepare demo for client meeting. Next meeting scheduled for Jan 24.",
                sender="scrum.master@company.com",
                recipient="dev-team@company.com",
                timestamp="2024-01-17T09:15:00Z"
            ),
            EmailData(
                message_id="msg_004",
                subject="Client Feedback - Website Redesign",
                content="The client has provided positive feedback on the initial website redesign mockups. They particularly liked the new navigation structure and color scheme. However, they requested changes to the footer layout and want to add a testimonials section on the homepage. Please incorporate these changes by next Tuesday.",
                sender="client.relations@company.com",
                recipient="design-team@company.com",
                timestamp="2024-01-18T16:20:00Z"
            ),
            EmailData(
                message_id="msg_005",
                subject="Security Alert - System Maintenance",
                content="IMPORTANT: Scheduled system maintenance will occur this Saturday from 2 AM to 6 AM EST. All services will be temporarily unavailable during this time. Please ensure all critical work is completed before the maintenance window. Emergency contact: IT Support at ext. 5555.",
                sender="it.admin@company.com", 
                recipient="all-staff@company.com",
                timestamp="2024-01-19T11:00:00Z"
            )
        ]
        self._emails = sample_emails
    
    def search_emails(self, keywords: List[str], inbox: Optional[str] = None, 
                     sent_before: Optional[str] = None) -> List[EmailData]:
        """Search emails by keywords."""
        results = []
        for email in self._emails:
            if email.matches_keywords(keywords):
                results.append(email)
        return results
    
    def get_email_by_id(self, message_id: str) -> Optional[EmailData]:
        """Retrieve email by message ID."""
        for email in self._emails:
            if email.message_id == message_id:
                return email
        return None
    
    def get_all_emails(self) -> List[EmailData]:
        """Get all emails."""
        return self._emails.copy()
    
    def add_email(self, email: EmailData) -> None:
        """Add a new email."""
        self._emails.append(email)
    
    def save_to_file(self, filename: Optional[str] = None) -> None:
        """Save emails to JSON file."""
        file_path = filename or self.data_file
        email_dicts = [email.to_dict() for email in self._emails]
        with open(file_path, 'w') as f:
            json.dump(email_dicts, f, indent=2)
    
    def load_from_file(self, filename: Optional[str] = None) -> None:
        """Load emails from JSON file."""
        file_path = filename or self.data_file
        try:
            with open(file_path, 'r') as f:
                email_dicts = json.load(f)
                self._emails = [EmailData(**email_dict) for email_dict in email_dicts]
        except FileNotFoundError:
            print(f"File {file_path} not found. Using sample data.")
            self.load_sample_data()

# Global email service instance
email_service = EmailService()