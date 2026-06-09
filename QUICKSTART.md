# Quick Start Guide

Get the Voice Call Center AI running in 5 minutes.

## Prerequisites

- Python 3.10+
- API keys for:
  - Twilio (phone number)
  - Anthropic (Claude)
  - Deepgram (STT)
  - ElevenLabs (TTS)

## 1. Setup

```bash
cd voice-call-center

# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

## 2. Install & Run

### Quick Start Script (Recommended for Mac)

```bash
./start.sh
```

The script handles virtual environment setup and dependency installation.

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

## 3. Verify It Works

```bash
# In another terminal
curl http://localhost:8000/health

# Should return:
# {"status":"ok","service":"Voice Call Center AI","active_calls":0}
```

## 4. Configure Twilio

1. Go to [Twilio Console](https://console.twilio.com)
2. Select your phone number
3. Under Voice Configuration, set webhook URL:
   - For local testing: Use [ngrok](https://ngrok.com)
   ```bash
   ngrok http 8000
   # Copy the HTTPS URL: https://xxxxx.ngrok.io/incoming-call
   ```
   - For production: Use your domain: `https://yourdomain.com/incoming-call`

## 5. Test a Call

Call your Twilio phone number and you should hear the welcome message!

## Common Issues

### "API key not found"
- Check `.env` file exists in project root
- Verify all keys are set (no blank values)

### Port 8000 already in use
```bash
# Use different port
PORT=8001 python main.py

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Twilio webhook not connecting
- Verify ngrok is running: `ngrok http 8000`
- Check webhook URL in Twilio console
- Look for errors in application logs

## Next Steps

1. **Customize the prompt**: Edit `CALL_CENTER_TYPE` in `.env`
   - Options: `customer_service`, `technical_support`, `appointment_scheduling`, `billing`, `sales`

2. **Change voice**: Update `VOICE_ID` in `.env`
   - See CONFIGURATION.md for voice options

3. **Deploy to production**: See DEPLOYMENT.md

4. **Monitor calls**: Visit `http://localhost:8000/docs` for API documentation

## Production Deployment

### Docker (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

### Mac mini / Linux

```bash
# Copy start script to systemd/launchd
# See DEPLOYMENT.md for full instructions

# Or use Docker as above
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/incoming-call` | POST | Twilio webhook for incoming calls |
| `/process-input` | POST | Process speech and respond |
| `/calls` | GET | List active calls |
| `/calls/{call_sid}` | GET | Get call details |
| `/docs` | GET | API documentation |

## File Structure

```
voice-call-center/
├── main.py              # FastAPI application
├── requirements.txt     # Dependencies
├── .env                 # Configuration (you create this)
├── config/
│   └── settings.py      # Settings management
├── services/
│   ├── call_manager.py  # Call orchestration
│   ├── llm.py           # Claude integration
│   ├── speech_to_text.py    # Deepgram STT
│   ├── text_to_speech.py    # ElevenLabs TTS
│   ├── monitoring.py    # Metrics tracking
│   ├── storage.py       # Call data persistence
│   └── prompts.py       # System prompts
├── data/                # Call recordings & data
├── logs/                # Application logs
└── docs/
    ├── README.md        # Full documentation
    ├── DEPLOYMENT.md    # Deployment guide
    └── CONFIGURATION.md # Configuration options
```

## Monitoring

### View Active Calls
```bash
curl http://localhost:8000/calls
```

### View Logs (if running with nohup)
```bash
tail -f logs/app.log
```

### Docker Monitoring
```bash
docker-compose logs -f voice-call-center
```

## Performance Tips

- For slow connections: Increase `REQUEST_TIMEOUT` to 45 seconds
- For high volume: Use Docker or systemd to restart on crash
- Monitor API usage: Check Deepgram, ElevenLabs, and Anthropic dashboards

## Getting Help

- Check logs for error messages
- See TROUBLESHOOTING.md (in DEPLOYMENT.md)
- Visit API docs at `http://localhost:8000/docs`
- Review code comments in individual service files

## What's Happening When You Get a Call?

1. **User calls** → Twilio receives call
2. **Twilio webhook** → Sends POST to `/incoming-call`
3. **Welcome message** → System says greeting
4. **Voice input** → User speaks
5. **Transcription** → Deepgram converts to text
6. **LLM processing** → Claude generates response
7. **Audio synthesis** → ElevenLabs converts to speech
8. **Response** → Twilio plays audio back to user
9. **Loop** → Repeat from step 4 until user hangs up

All in under 3 seconds per interaction!

---

**Ready to launch?** Run `./start.sh` and call your Twilio number! 🚀
