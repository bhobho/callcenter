import os
from elevenlabs import Client, VoiceSettings

class TextToSpeechService:
    def __init__(self):
        self.client = Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella voice (can be changed)
        self.model_id = "eleven_monolingual_v1"

    def set_voice(self, voice_id: str):
        """Set the voice to use for TTS"""
        self.voice_id = voice_id

    def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech and return audio bytes

        Args:
            text: Text to convert to speech

        Returns:
            Audio bytes in MP3 format
        """
        try:
            audio = self.client.generate(
                text=text,
                voice=self.voice_id,
                model=self.model_id,
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                )
            )

            # Convert generator to bytes
            audio_bytes = b''.join(audio)
            return audio_bytes
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            raise

    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            voices = self.client.voices.get_all()
            return [{"voice_id": v.voice_id, "name": v.name} for v in voices.voices]
        except Exception as e:
            print(f"Error fetching voices: {e}")
            raise
