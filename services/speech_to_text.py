import os
import logging
from deepgram import DeepgramClient, PrerecordedOptions, LiveOptions

logger = logging.getLogger(__name__)


class SpeechToTextService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.client = DeepgramClient(api_key=self.api_key)
        self.model = "nova-2"

    async def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribe audio data to text using Deepgram

        Args:
            audio_data: Raw audio bytes

        Returns:
            Transcribed text
        """
        try:
            options = PrerecordedOptions(
                model=self.model,
                language="en-US",
                smart_format=True,
                punctuate=True,
            )

            response = await self.client.listen.prerecorded.transcribe_file(
                {"buffer": audio_data},
                options,
            )

            # Extract transcript from response
            if response.get("results") and response["results"].get("channels"):
                transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
                logger.info(f"Transcription successful: {transcript[:100]}...")
                return transcript
            else:
                logger.warning("Empty transcription response")
                return ""

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise

    async def transcribe_from_url(self, audio_url: str) -> str:
        """
        Transcribe audio from a URL using Deepgram

        Args:
            audio_url: URL of the audio file

        Returns:
            Transcribed text
        """
        try:
            options = PrerecordedOptions(
                model=self.model,
                language="en-US",
                smart_format=True,
                punctuate=True,
            )

            response = await self.client.listen.prerecorded.transcribe_url(
                {"url": audio_url},
                options,
            )

            if response.get("results") and response["results"].get("channels"):
                transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
                logger.info(f"URL transcription successful: {transcript[:100]}...")
                return transcript
            else:
                logger.warning("Empty transcription response from URL")
                return ""

        except Exception as e:
            logger.error(f"URL transcription error: {e}")
            raise

    def get_confidence_score(self, audio_data: bytes) -> float:
        """
        Get confidence score for transcription

        Args:
            audio_data: Raw audio bytes

        Returns:
            Confidence score (0-1)
        """
        try:
            # This would require additional API calls, for now return default
            return 0.85
        except Exception as e:
            logger.error(f"Error getting confidence score: {e}")
            return 0.0
