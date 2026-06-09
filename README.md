# Voice-Based Call Center AI

A real-time voice call center application where users can call in and interact with an AI-powered agent using natural language. The system handles speech-to-text transcription, LLM processing, and text-to-speech response generation.

## Architecture

- **Call Handling**: Twilio for VoIP/telephony
- **Speech-to-Text**: Deepgram for real-time transcription
- **LLM**: Claude (Anthropic API) for intelligent responses
- **Text-to-Speech**: ElevenLabs for natural voice output
- **Server**: FastAPI + Uvicorn

## Setup

1. Clone and navigate to the project:
```bash
cd voice-call-center
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /health` - Health check
- `POST /incoming-call` - Handle incoming Twilio calls
- `POST /process-speech` - Process and respond to user speech

## Configuration

Required environment variables:
- `TWILIO_ACCOUNT_SID` - Your Twilio account ID
- `TWILIO_AUTH_TOKEN` - Your Twilio auth token
- `TWILIO_PHONE_NUMBER` - Your Twilio phone number
- `ANTHROPIC_API_KEY` - Claude API key
- `DEEPGRAM_API_KEY` - Deepgram API key for speech-to-text
- `ELEVENLABS_API_KEY` - ElevenLabs API key for text-to-speech

## Development

To expose the local server for Twilio webhooks, use ngrok:
```bash
ngrok http 8000
# Update Twilio webhook URL to: https://your-ngrok-url.ngrok.io/incoming-call
```

## Next Steps

- [ ] Implement real-time speech-to-text pipeline
- [ ] Integrate Claude API for LLM responses
- [ ] Set up text-to-speech streaming
- [ ] Add call state management
- [ ] Implement error handling and fallbacks
- [ ] Add logging and monitoring
- [ ] Create system prompts for call handling
