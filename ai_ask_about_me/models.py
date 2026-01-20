"""Pydantic models for tool arguments and responses."""

from pydantic import BaseModel, Field


class RecordUserDetailsArgs(BaseModel):
    """Arguments for recording user contact details."""
    
    email: str | None = Field(..., description="The email address of this user")
    name: str | None = Field(default="Name not provided", description="The user's name, if they provided it")
    notes: str | None = Field(default="not provided", description="Any additional information about the conversation that's worth recording to give context")


class RecordUnknownQuestionArgs(BaseModel):
    """Arguments for recording an unanswered question."""
    
    question: str = Field(..., description="The question that couldn't be answered")


class ToolResult(BaseModel):
    """Standard tool result response."""
    
    recorded: str = "ok"
