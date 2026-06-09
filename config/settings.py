from pydantic_settings import BaseSettings
from services.prompts import get_system_prompt


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
    # Port 8000 is often taken by Docker on macOS; default to 8080
    port: int = 8080
    host: str = "0.0.0.0"
    debug: bool = False

    # Call Center Configuration
    call_center_type: str = "customer_service"  # customer_service, technical_support, appointment_scheduling, billing, sales
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"  # ElevenLabs voice ID
    max_call_duration: int = 3600  # 1 hour in seconds
    request_timeout: int = 30  # seconds

    # System Prompt - dynamically loaded based on call_center_type
    @property
    def system_prompt(self) -> str:
        return get_system_prompt(self.call_center_type)

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
try:
    settings = Settings()
except Exception as e:
    # Fallback for development without .env file
    print(f"Warning: Could not load settings from .env: {e}")
    settings = None
