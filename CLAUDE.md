# Voice Call Center AI - Development Guide

## Project Overview

A voice-based call center application that enables real-time conversations between users and an AI agent powered by Claude. The system handles the complete pipeline: call reception → speech-to-text → LLM processing → text-to-speech.

## Tech Stack

- **FastAPI**: Web framework for handling Twilio webhooks
- **Twilio**: VoIP and telephony
- **Deepgram**: Speech-to-text transcription
- **Claude API**: Large language model for intelligent responses
- **ElevenLabs**: Text-to-speech voice synthesis

## Project Structure

```
voice-call-center/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration management
├── services/
│   ├── __init__.py
│   ├── speech_to_text.py  # Deepgram integration
│   ├── llm.py             # Claude API integration
│   └── text_to_speech.py  # ElevenLabs integration
└── utils/
    ├── __init__.py
    └── helpers.py         # Utility functions
```

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file** from template:
   ```bash
   cp .env.example .env
   # Fill in your API credentials
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Expose to internet** (for Twilio webhooks):
   ```bash
   ngrok http 8000
   ```

5. **Configure Twilio webhook**:
   - Set your webhook URL in Twilio dashboard to: `https://your-ngrok-url/incoming-call`

## Development Notes

### Latency Optimization
- Current implementation uses sequential processing (STT → LLM → TTS)
- For production, consider:
  - Streaming audio processing to reduce end-to-end latency
  - Voice Activity Detection (VAD) to detect when user stops speaking
  - Parallel processing where possible
  - Prompt caching for frequently used system prompts

### Integration Points
- **Twilio**: Handles call signaling and audio streaming
- **Deepgram**: Converts user speech to text in real-time
- **Claude**: Generates contextual responses with conversation history
- **ElevenLabs**: Converts responses back to natural-sounding speech

### Next Steps
1. Implement real-time streaming for speech-to-text
2. Add call state management (collect transcript, call duration, etc.)
3. Implement error handling and fallback responses
4. Add call recording and analytics
5. Create agent personality system for different call types
6. Add queue management for multiple concurrent calls

## API Endpoints

- `GET /health` - Health check
- `POST /incoming-call` - Initial call handler
- `POST /process-speech` - Process user input and generate response

## Testing

Use curl or Postman to test endpoints locally before configuring Twilio:
```bash
curl http://localhost:8000/health
```

## Monitoring & Logging

- Logs are printed to stdout
- Call data should be logged for analytics and debugging
- Monitor API rate limits for Deepgram and ElevenLabs
