"""Constants and configuration for the AI Ask About Me application."""

# Model configuration
MODEL_NAME = "gpt-4o-mini"

# File paths
LINKEDIN_PDF_PATH = "assets/my_cv.pdf"
SUMMARY_TXT_PATH = "assets/summary_about_me.txt"

# Person name
PERSON_NAME = "Armel Ardael"


def build_system_prompt(name: str, summary: str, linkedin: str) -> str:
    """
    Build the system prompt for the AI agent.
    
    Args:
        name: The name of the person the AI is representing
        summary: Summary text about the person
        linkedin: LinkedIn profile text extracted from PDF
        
    Returns:
        Complete system prompt string
    """
    system_prompt = (
        f"You are acting as {name}. You are answering questions on {name}'s website, "
        f"particularly questions related to {name}'s career, background, skills and experience. "
        f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. "
        f"You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. "
        f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        f"If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. "
        f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
    )
    
    system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
    system_prompt += f"With this context, please chat with the user, always staying in character as {name}."
    
    return system_prompt
