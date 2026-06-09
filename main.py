from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import XMLResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv
import logging
from config.settings import settings
from services.call_manager import CallManager
from utils.helpers import setup_logging

load_dotenv()

# Setup logging
logger = setup_logging()

app = FastAPI(title="Voice Call Center AI")

# Initialize Twilio client
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

# Call manager for handling call state
call_manager = CallManager()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Voice Call Center AI application")
    await call_manager.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Voice Call Center AI application")
    await call_manager.cleanup()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Voice Call Center AI",
        "active_calls": call_manager.get_active_calls_count()
    }


@app.post("/incoming-call")
async def incoming_call(request: Request):
    """Handle incoming Twilio call"""
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        from_number = form_data.get("From")
        to_number = form_data.get("To")

        logger.info(f"Incoming call - SID: {call_sid}, From: {from_number}")

        # Initialize call in manager
        call_manager.start_call(call_sid, from_number, to_number)

        response = VoiceResponse()

        # Start recording the call for later reference
        response.record(
            action="/call-complete",
            method="POST",
            max_length=3600,
            record_status_callback="/record-status",
            record_status_callback_method="POST"
        )

        # Welcome message and ask for input
        response.say(
            "Hello! Welcome to our AI powered call center. Please tell me how I can help you today.",
            voice="alice"
        )

        # Gather speech input
        gather = response.gather(
            input="speech",
            action="/process-input",
            method="POST",
            timeout=5,
            max_speech_time=30,
            speech_model="default"
        )

        return XMLResponse(content=str(response))

    except Exception as e:
        logger.error(f"Error in incoming_call: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, there was an error. Please try again later.")
        response.hangup()
        return XMLResponse(content=str(response))


@app.post("/process-input")
async def process_input(request: Request):
    """Process user speech input and generate AI response"""
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        speech_result = form_data.get("SpeechResult", "")
        confidence = float(form_data.get("Confidence", 0.0))

        logger.info(f"Processing speech for {call_sid}: '{speech_result}' (confidence: {confidence})")

        if not speech_result or confidence < 0.3:
            logger.warning(f"Low confidence or empty speech for {call_sid}")
            response = VoiceResponse()
            response.say("I didn't catch that. Could you please repeat?", voice="alice")
            gather = response.gather(
                input="speech",
                action="/process-input",
                method="POST",
                timeout=5,
                max_speech_time=30,
            )
            return XMLResponse(content=str(response))

        # Get AI response
        ai_response = await call_manager.get_ai_response(call_sid, speech_result)

        logger.info(f"AI response for {call_sid}: {ai_response}")

        response = VoiceResponse()
        response.say(ai_response, voice="alice")

        # Ask for follow-up input or end call
        response.say("Is there anything else I can help you with?", voice="alice")

        gather = response.gather(
            input="speech",
            action="/process-input",
            method="POST",
            timeout=5,
            max_speech_time=30,
        )

        # Fallback to hangup if no input
        response.hangup()

        return XMLResponse(content=str(response))

    except Exception as e:
        logger.error(f"Error in process_input: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, I encountered an error processing your request.", voice="alice")
        response.hangup()
        return XMLResponse(content=str(response))


@app.post("/call-complete")
async def call_complete(request: Request):
    """Handle call completion"""
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        recording_url = form_data.get("RecordingUrl")

        logger.info(f"Call completed - SID: {call_sid}, Recording: {recording_url}")

        # Finalize call in manager
        call_data = call_manager.end_call(call_sid, recording_url)

        logger.info(f"Call summary: {call_data}")

        response = VoiceResponse()
        response.say("Thank you for calling. Goodbye!", voice="alice")
        response.hangup()

        return XMLResponse(content=str(response))

    except Exception as e:
        logger.error(f"Error in call_complete: {str(e)}")
        response = VoiceResponse()
        response.hangup()
        return XMLResponse(content=str(response))


@app.post("/record-status")
async def record_status(request: Request):
    """Receive recording status updates from Twilio"""
    try:
        form_data = await request.form()
        recording_sid = form_data.get("RecordingSid")
        recording_status = form_data.get("RecordingStatus")

        logger.info(f"Recording status - SID: {recording_sid}, Status: {recording_status}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error in record_status: {str(e)}")
        return {"status": "error"}


@app.get("/calls")
def get_active_calls():
    """Get list of active calls"""
    return {
        "active_calls": call_manager.get_active_calls_count(),
        "calls": call_manager.get_call_details()
    }


@app.get("/calls/{call_sid}")
def get_call_details(call_sid: str):
    """Get details of a specific call"""
    details = call_manager.get_call_details_by_sid(call_sid)
    if not details:
        raise HTTPException(status_code=404, detail="Call not found")
    return details


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )
