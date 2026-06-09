import logging

def setup_logging():
    """Set up logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def sanitize_text(text: str) -> str:
    """
    Sanitize text for TTS to avoid issues with special characters

    Args:
        text: Raw text

    Returns:
        Sanitized text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Limit length for reasonable audio output
    if len(text) > 1000:
        text = text[:1000] + "..."
    return text

def format_call_log(call_sid: str, from_number: str, to_number: str, duration: int, transcript: str):
    """Format call information for logging"""
    return {
        "call_sid": call_sid,
        "from": from_number,
        "to": to_number,
        "duration_seconds": duration,
        "transcript": transcript,
    }
