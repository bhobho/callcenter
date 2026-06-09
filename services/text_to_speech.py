import os
import logging
from elevenlabs import Client, VoiceSettings, stream

logger = logging.getLogger(__name__)


class TextToSpeechService:
    def __init__(self):
        self.client = Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
        # Professional voices for call center
        self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella voice
        self.model_id = "eleven_multilingual_v2"
        self.voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
        )

    def set_voice(self, voice_id: str):
        """Set the voice to use for TTS"""
        self.voice_id = voice_id
        logger.info(f"Voice changed to: {voice_id}")

    def synthesize(self, text: str, format: str = "mp3_22050_32") -> bytes:
        """
        Convert text to speech and return audio bytes

        Args:
            text: Text to convert to speech
            format: Audio format (default: mp3_22050_32 for lower bandwidth)

        Returns:
            Audio bytes in specified format
        """
        try:
            if not text or len(text.strip()) == 0:
                logger.warning("Empty text provided to synthesize")
                return b''

            # Limit text length to avoid issues
            if len(text) > 1000:
                logger.warning("Text truncated to 1000 chars")
                text = text[:1000]

            audio_generator = self.client.generate(
                text=text,
                voice=self.voice_id,
                model=self.model_id,
                voice_settings=self.voice_settings,
            )

            # Stream and convert to bytes
            audio_bytes = b''.join(audio_generator)
            logger.info(f"Audio synthesized successfully: {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            raise

    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            voices = self.client.voices.get_all()
            voice_list = [
                {"voice_id": v.voice_id, "name": v.name}
                for v in voices.voices
            ]
            logger.info(f"Retrieved {len(voice_list)} available voices")
            return voice_list
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            raise

    def test_voice(self, text: str = "Hello, this is a test. How can I help you?") -> bytes:
        """Test the current voice configuration"""
        logger.info(f"Testing voice: {self.voice_id}")
        return self.synthesize(text)
