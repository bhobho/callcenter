from fastapi import FastAPI, Request
from fastapi.responses import XMLResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/incoming-call")
async def incoming_call(request: Request):
    """Handle incoming Twilio call"""
    response = VoiceResponse()

    # Gather user input
    gather = response.gather(
        num_digits=1,
        action="/process-speech",
        method="POST",
        timeout=3
    )
    gather.say("Hello, this is an AI powered call center. Please speak your inquiry.")

    return XMLResponse(content=str(response))


@app.post("/process-speech")
async def process_speech(request: Request):
    """Process user speech and generate LLM response"""
    form_data = await request.form()

    # TODO: Implement speech-to-text, LLM processing, and text-to-speech
    response = VoiceResponse()
    response.say("Thank you for calling. How can I help you?")
    response.hangup()

    return XMLResponse(content=str(response))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
