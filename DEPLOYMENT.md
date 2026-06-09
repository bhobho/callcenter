# Deployment Guide for macOS / Mac mini

This guide covers deploying the Voice Call Center AI application on macOS, including both development and production setups.

## Prerequisites

- macOS 10.14 or later
- Python 3.10 or later
- Internet connection for API calls
- Twilio account with phone number
- Anthropic API key
- Deepgram API key
- ElevenLabs API key

## Installation

### 1. Clone and Set Up

```bash
cd /Users/neerajpandey/Dev/cc/voice-call-center
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` and add your credentials:

```bash
nano .env
```

Required variables:
- `TWILIO_ACCOUNT_SID` - Your Twilio account ID
- `TWILIO_AUTH_TOKEN` - Your Twilio authentication token
- `TWILIO_PHONE_NUMBER` - Your Twilio phone number
- `ANTHROPIC_API_KEY` - Claude API key
- `DEEPGRAM_API_KEY` - Deepgram API key
- `ELEVENLABS_API_KEY` - ElevenLabs API key

### 3. Quick Start (Development)

```bash
./start.sh
```

This script will:
- Create a Python virtual environment
- Install dependencies
- Start the application on port 8000

The API will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

## Production Deployment

### Option 1: Docker (Recommended)

```bash
# Build Docker image
docker build -t voice-call-center .

# Run with Docker
docker run -p 8000:8000 \
  -e TWILIO_ACCOUNT_SID=your_sid \
  -e TWILIO_AUTH_TOKEN=your_token \
  -e TWILIO_PHONE_NUMBER=your_number \
  -e ANTHROPIC_API_KEY=your_key \
  -e DEEPGRAM_API_KEY=your_key \
  -e ELEVENLABS_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  voice-call-center
```

Or with Docker Compose:

```bash
docker-compose up -d
```

### Option 2: systemd Service (macOS Launchd)

Create a launchd plist file at:
```
~/Library/LaunchAgents/com.voicecallcenter.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.voicecallcenter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/neerajpandey/Dev/cc/voice-call-center/start.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/neerajpandey/Dev/cc/voice-call-center</string>
    <key>StandardOutPath</key>
    <string>/Users/neerajpandey/Dev/cc/voice-call-center/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/neerajpandey/Dev/cc/voice-call-center/logs/stderr.log</string>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

Then load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.voicecallcenter.plist
```

### Option 3: Manual systemd (for non-Mac Linux servers)

Create `/etc/systemd/system/voice-call-center.service`:

```ini
[Unit]
Description=Voice Call Center AI
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/voice-call-center
Environment="PATH=/home/pi/voice-call-center/venv/bin"
ExecStart=/home/pi/voice-call-center/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable voice-call-center
sudo systemctl start voice-call-center
```

## Exposing to the Internet

### Using ngrok (Development)

```bash
ngrok http 8000
```

Copy the HTTPS URL and configure in Twilio webhook:
```
https://your-ngrok-url.ngrok.io/incoming-call
```

### Using a Reverse Proxy (Production)

With Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring

### Check Service Status

```bash
# Docker
docker ps | grep voice-call-center

# Launchd (macOS)
launchctl list | grep voicecallcenter

# Systemd
systemctl status voice-call-center
```

### View Logs

```bash
# Docker
docker logs voice-call-center -f

# Launchd
tail -f ~/Library/LaunchAgents/../logs/stdout.log

# Systemd
journalctl -u voice-call-center -f
```

### Health Check

```bash
curl http://localhost:8000/health
```

## API Endpoints

- `GET /health` - Health status
- `POST /incoming-call` - Twilio incoming call webhook
- `POST /process-input` - Process speech input
- `POST /call-complete` - Call completion webhook
- `GET /calls` - List active calls
- `GET /calls/{call_sid}` - Get call details
- `GET /docs` - API documentation (Swagger UI)

## Performance Tuning

### For Mac mini

1. **Memory Management**
   - Monitor memory usage: `top -n 1 | head -20`
   - Adjust uvicorn workers based on available RAM

2. **Concurrent Calls**
   - Update `main.py` uvicorn config:
   ```python
   uvicorn.run(
       app,
       host=settings.host,
       port=settings.port,
       workers=4,  # Adjust based on CPU cores
       loop="uvloop"  # Faster event loop
   )
   ```

3. **API Rate Limiting**
   - Consider caching responses
   - Implement request queuing for high volume

## Troubleshooting

### Connection Issues

```bash
# Test Twilio connectivity
python -c "from twilio.rest import Client; print('OK')"

# Test API keys
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/health
```

### Audio Quality Issues

- Adjust Deepgram model in `services/speech_to_text.py`
- Try different ElevenLabs voices
- Check network bandwidth

### Performance Issues

- Monitor API response times: `grep "Response generated" logs/*.log`
- Reduce max_tokens in LLM service
- Implement response caching

## Backup and Recovery

### Data Backup

```bash
# Backup call data
cp -r data/ data_backup_$(date +%Y%m%d)

# Automated backup (add to crontab)
0 2 * * * cp -r ~/voice-call-center/data ~/backups/data_$(date +\%Y\%m\%d)
```

### Database Reset

```bash
rm -rf data/*.json
```

## Updating the Application

```bash
git pull origin main
pip install -r requirements.txt --upgrade
systemctl restart voice-call-center
```

## Security Considerations

1. **API Keys**: Use environment variables, never commit `.env`
2. **HTTPS**: Use SSL certificate for production (Let's Encrypt)
3. **Firewall**: Restrict access to port 8000
4. **Authentication**: Consider adding API key authentication
5. **Call Recording**: Ensure compliance with local laws

## Support

For issues, check:
- Application logs in `logs/` directory
- API docs at `/docs` endpoint
- Twilio webhook logs in Twilio dashboard
