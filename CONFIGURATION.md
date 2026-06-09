# Configuration Guide

## Environment Variables

All configuration is managed through environment variables defined in `.env` file.

### Required Configuration

#### Twilio

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+16175551313
```

Get these from [Twilio Dashboard](https://console.twilio.com):
1. Go to Account Info
2. Copy Account SID and Auth Token
3. Go to Phone Numbers → Manage Numbers
4. Copy your phone number

#### Anthropic (Claude API)

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get from [Anthropic Console](https://console.anthropic.com):
1. Create an API key
2. Copy the full key

#### Deepgram (Speech-to-Text)

```env
DEEPGRAM_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get from [Deepgram Console](https://console.deepgram.com):
1. Go to API Keys
2. Create new key
3. Copy the key

#### ElevenLabs (Text-to-Speech)

```env
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get from [ElevenLabs Dashboard](https://elevenlabs.io/app):
1. Go to Account → Profile
2. Copy API Key

### Optional Configuration

#### Server Settings

```env
# Port to run server on (default: 8000)
PORT=8000

# Host to bind to (default: 0.0.0.0)
HOST=0.0.0.0

# Debug mode (default: false)
DEBUG=false
```

#### Call Center Configuration

```env
# Type of call center: customer_service, technical_support, appointment_scheduling, billing, sales
# (default: customer_service)
CALL_CENTER_TYPE=customer_service

# ElevenLabs Voice ID (default: EXAVITQu4vr4xnSDxMaL - Bella)
# Get available voices from: https://elevenlabs.io/docs/voices
VOICE_ID=EXAVITQu4vr4xnSDxMaL

# Maximum call duration in seconds (default: 3600)
MAX_CALL_DURATION=3600

# Request timeout in seconds (default: 30)
REQUEST_TIMEOUT=30
```

## Voice IDs

Available ElevenLabs voices:

| Voice ID | Name | Type |
|----------|------|------|
| `EXAVITQu4vr4xnSDxMaL` | Bella | Professional Female |
| `21m00Tcm4TlvDq8ikWAM` | Rachel | Warm Female |
| `AZnzlk1UV00M4xWNhgehT` | Clyde | Friendly Male |
| `EZ1be7o6ybVAHFFRtoWJ` | Adam | Strong Male |
| `TX3LPaxmHKQFdXL7f6qO` | Domi | Bold Female |

See [ElevenLabs Voices](https://elevenlabs.io/docs/voices) for complete list.

## Call Center Types

### Customer Service (Default)
```env
CALL_CENTER_TYPE=customer_service
```
Best for: General customer support, inquiries, complaints

**System Prompt Focus:**
- Professional and empathetic
- Clear and concise responses
- Offers solutions or escalation

### Technical Support
```env
CALL_CENTER_TYPE=technical_support
```
Best for: Troubleshooting, technical assistance

**System Prompt Focus:**
- Systematic diagnosis
- Step-by-step guidance
- Simple technical explanations

### Appointment Scheduling
```env
CALL_CENTER_TYPE=appointment_scheduling
```
Best for: Booking appointments, managing schedules

**System Prompt Focus:**
- Availability suggestions
- Time confirmation
- Clear appointment details

### Billing Inquiries
```env
CALL_CENTER_TYPE=billing
```
Best for: Billing questions, invoices, payments

**System Prompt Focus:**
- Clear billing explanations
- Privacy protection
- Payment options

### Sales Support
```env
CALL_CENTER_TYPE=sales
```
Best for: Product sales, upselling

**System Prompt Focus:**
- Feature highlighting
- Benefit explanations
- Purchase guidance

## Twilio Setup

### 1. Create Account
- Go to [Twilio.com](https://www.twilio.com)
- Sign up for free account

### 2. Get Credentials
- Account SID: Visible on dashboard
- Auth Token: Account Info section

### 3. Get Phone Number
- Phone Numbers → Manage → Buy a Number
- Choose number type and region

### 4. Configure Webhook
- Phone Numbers → Manage Numbers
- Select your number
- Under Voice Configuration:
  - A Call Comes In: Select `Webhook`
  - URL: `https://your-domain.com/incoming-call`
  - HTTP POST
  - Save

### Testing with ngrok

For development, expose localhost to internet:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000

# You'll get a URL like: https://abcd1234.ngrok.io
# Configure in Twilio: https://abcd1234.ngrok.io/incoming-call
```

## Performance Tuning

### For Low Resource Systems

```env
# Reduce LLM context tokens
# Edit services/llm.py - max_tokens=200

# Increase request timeout for slower API
REQUEST_TIMEOUT=45

# Use lighter voice model
# Edit services/speech_to_text.py - model="nova"
```

### For High Volume

```env
# Configure multiple workers in Dockerfile
# ARG WORKERS=4
# CMD ["gunicorn", "-w", "${WORKERS}", ...]

# Implement caching
# Edit services/llm.py - add response cache
```

## Advanced Configuration

### Custom System Prompts

Edit `.env` with custom prompt (advanced users):

```env
# Add custom system prompt (keep under 1000 chars for voice interaction)
SYSTEM_PROMPT="You are a helpful AI assistant..."
```

Or modify `services/prompts.py` for new scenario types.

### API Rate Limiting

Deepgram: 
- Free: 50,000 minutes/month
- Check usage: [Deepgram Dashboard](https://console.deepgram.com/usage)

ElevenLabs:
- Free: 10,000 characters/month
- Check usage: [ElevenLabs Account](https://elevenlabs.io/app)

Anthropic:
- Monitor costs: [Anthropic Dashboard](https://console.anthropic.com)

## Troubleshooting

### API Authentication Errors

```
Error: Invalid API key
```
- Check `.env` has correct key
- Verify key is not expired
- Copy full key including prefix

### Missing Credentials

```
Error: TWILIO_ACCOUNT_SID not found
```
- Ensure `.env` file exists in project root
- All required variables must be set
- No empty values

### Port Already in Use

```
Address already in use: ('0.0.0.0', 8000)
```
- Change PORT: `PORT=8001`
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`

### Timeout Issues

```
timeout waiting for response
```
- Increase REQUEST_TIMEOUT
- Check internet connection
- Verify API keys are valid

## Security Best Practices

1. **Never commit `.env`**
   - Add to `.gitignore`
   - Keep credentials local only

2. **Rotate API keys regularly**
   - Set calendar reminders
   - Update all references

3. **Use environment-specific credentials**
   - Dev/Staging/Production keys
   - Different Twilio numbers

4. **Monitor usage**
   - Check API dashboards regularly
   - Set usage alerts if available

5. **Restrict access**
   - Use firewall rules
   - Limit webhook access to Twilio IPs

## Configuration Examples

### Development
```env
CALL_CENTER_TYPE=customer_service
DEBUG=true
PORT=8000
REQUEST_TIMEOUT=30
```

### Production
```env
CALL_CENTER_TYPE=customer_service
DEBUG=false
PORT=8000
REQUEST_TIMEOUT=15
MAX_CALL_DURATION=1800
```

### High Volume
```env
CALL_CENTER_TYPE=customer_service
REQUEST_TIMEOUT=20
MAX_CALL_DURATION=600
```

## Support

- Twilio Docs: https://www.twilio.com/docs/
- Deepgram Docs: https://developers.deepgram.com/
- ElevenLabs Docs: https://elevenlabs.io/docs/
- Anthropic Docs: https://docs.anthropic.com/
