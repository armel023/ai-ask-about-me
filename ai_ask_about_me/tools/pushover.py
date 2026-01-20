"""Pushover notification utility."""

import os
import requests


def push(text: str) -> None:
    """
    Send a notification via Pushover API.
    
    Args:
        text: The message text to send
    """
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )
