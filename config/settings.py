from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Twilio Configuration
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

    # Anthropic Configuration
    anthropic_api_key: str

    # Deepgram Configuration
    deepgram_api_key: str

    # ElevenLabs Configuration
    elevenlabs_api_key: str

    # Server Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    debug: bool = False

    # System Prompt
    system_prompt: str = """You are a professional and helpful customer service representative for a call center.
    You should:
    - Be friendly and professional
    - Listen carefully to customer requests
    - Provide clear and concise answers
    - Offer to help with additional requests
    - Handle common inquiries about billing, support, and general questions
    Keep responses concise and natural for voice conversation (aim for 1-3 sentences)."""

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
