import os
from deepgram import DeepgramClient, PrerecordedOptions

class SpeechToTextService:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.client = DeepgramClient(api_key=self.api_key)

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
                model="nova-2",
                language="en-US",
            )

            response = await self.client.listen.prerecorded.transcribe_file(
                {"buffer": audio_data},
                options,
            )

            # Extract transcript from response
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript
        except Exception as e:
            print(f"Transcription error: {e}")
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
                model="nova-2",
                language="en-US",
            )

            response = await self.client.listen.prerecorded.transcribe_url(
                {"url": audio_url},
                options,
            )

            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
