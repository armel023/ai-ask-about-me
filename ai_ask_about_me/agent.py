"""AI Agent class that handles chat interactions."""

import json
from openai import OpenAI
from pypdf import PdfReader

from ai_ask_about_me.constants import (
    MODEL_NAME,
    LINKEDIN_PDF_PATH,
    SUMMARY_TXT_PATH,
    PERSON_NAME,
    build_system_prompt,
)
from ai_ask_about_me.models import RecordUserDetailsArgs, RecordUnknownQuestionArgs
from ai_ask_about_me.tools import TOOL_REGISTRY, TOOLS


class MeAgent:
    """Agent that represents Armel Ardael and handles chat interactions."""

    def __init__(self):
        """Initialize the agent with OpenAI client and load personal data."""
        self.openai = OpenAI()
        self.name = PERSON_NAME
        
        # Load LinkedIn PDF
        reader = PdfReader(LINKEDIN_PDF_PATH)
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        
        # Load summary text
        with open(SUMMARY_TXT_PATH, "r", encoding="utf-8") as f:
            self.summary = f.read()

    def handle_tool_call(self, tool_calls):
        """
        Handle tool calls from OpenAI API response.
        
        Args:
            tool_calls: List of tool call objects from OpenAI
            
        Returns:
            List of tool result messages for the API
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            
            # Get tool function from registry
            tool_func = TOOL_REGISTRY.get(tool_name)
            if not tool_func:
                result = {}
            else:
                # Validate arguments with Pydantic models
                if tool_name == "record_user_details":
                    validated_args = RecordUserDetailsArgs(**arguments)
                    result = tool_func(
                        email=validated_args.email,
                        name=validated_args.name,
                        notes=validated_args.notes
                    )
                elif tool_name == "record_unknown_question":
                    validated_args = RecordUnknownQuestionArgs(**arguments)
                    result = tool_func(question=validated_args.question)
                else:
                    result = tool_func(**arguments)
            
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results
    
    def system_prompt(self) -> str:
        """
        Generate the system prompt for the AI agent.
        
        Returns:
            Complete system prompt string
        """
        return build_system_prompt(self.name, self.summary, self.linkedin)
    
    def chat(self, message, history):
        """
        Handle a chat message and return the assistant's response.
        
        Gradio's ChatInterface commonly supplies `history` as a list of (user, assistant) tuples.
        Some newer variants may supply OpenAI-style message dicts. Support both.
        
        Args:
            message: The current user message
            history: Chat history (either tuples or dicts)
            
        Returns:
            Assistant's response text
        """
        normalized_history = []

        # History as OpenAI-style dict messages: [{"role": "...", "content": "..."}, ...]
        if isinstance(history, list) and (len(history) == 0 or isinstance(history[0], dict)):
            normalized_history = history
        # History as Gradio tuples: [("hi", "hello"), ...]
        elif isinstance(history, list):
            for turn in history:
                if not isinstance(turn, (list, tuple)) or len(turn) != 2:
                    continue
                user_msg, assistant_msg = turn
                if user_msg is not None and str(user_msg).strip() != "":
                    normalized_history.append({"role": "user", "content": str(user_msg)})
                if assistant_msg is not None and str(assistant_msg).strip() != "":
                    normalized_history.append({"role": "assistant", "content": str(assistant_msg)})

        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + normalized_history
            + [{"role": "user", "content": message}]
        )
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
