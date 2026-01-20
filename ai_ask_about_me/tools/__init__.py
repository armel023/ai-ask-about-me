"""Tools package - contains tool functions, schemas, and registry."""

from ai_ask_about_me.tools.recording import record_user_details, record_unknown_question
from ai_ask_about_me.tools.schemas import TOOLS

# Tool registry mapping tool names to their functions
TOOL_REGISTRY = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}

__all__ = ["TOOL_REGISTRY", "TOOLS", "record_user_details", "record_unknown_question"]
