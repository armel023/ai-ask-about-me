"""Tool functions for recording user details and unknown questions."""

from ai_ask_about_me.models import ToolResult
from ai_ask_about_me.tools.pushover import push


def record_user_details(email: str, name: str | None = None, notes: str | None = None) -> dict:
    """
    Record user contact details via Pushover notification.
    
    Args:
        email: The user's email address
        name: The user's name (optional)
        notes: Additional context notes (optional)
        
    Returns:
        Tool result dictionary
    """
    if name is None:
        name = "Name not provided"
    if notes is None:
        notes = "not provided"
    
    push(f"Recording {name} with email {email} and notes {notes}")
    result = ToolResult()
    return result.model_dump()


def record_unknown_question(question: str) -> dict:
    """
    Record an unanswered question via Pushover notification.
    
    Args:
        question: The question that couldn't be answered
        
    Returns:
        Tool result dictionary
    """
    push(f"Recording {question}")
    result = ToolResult()
    return result.model_dump()
