import logging
from datetime import datetime
from typing import Dict, Optional
from services.llm import LLMService
from config.settings import settings

logger = logging.getLogger(__name__)


class CallManager:
    """Manages call state and coordinates services"""

    def __init__(self):
        self.active_calls: Dict[str, Dict] = {}
        self.llm_service = LLMService()
        self.llm_service.set_system_prompt(settings.system_prompt)

    async def initialize(self):
        """Initialize call manager"""
        logger.info("CallManager initialized")

    async def cleanup(self):
        """Clean up resources"""
        logger.info(f"Cleaning up {len(self.active_calls)} active calls")
        self.active_calls.clear()

    def start_call(self, call_sid: str, from_number: str, to_number: str):
        """Start a new call"""
        self.active_calls[call_sid] = {
            "call_sid": call_sid,
            "from": from_number,
            "to": to_number,
            "start_time": datetime.utcnow(),
            "transcript": [],
            "messages": [],
            "recording_url": None,
            "status": "active"
        }
        # Reset LLM conversation for new call
        self.llm_service.reset_conversation()
        logger.info(f"Call started: {call_sid} from {from_number}")

    def end_call(self, call_sid: str, recording_url: Optional[str] = None) -> Dict:
        """End a call and return summary"""
        if call_sid not in self.active_calls:
            logger.warning(f"Call {call_sid} not found in active calls")
            return {}

        call = self.active_calls[call_sid]
        call["end_time"] = datetime.utcnow()
        call["status"] = "completed"
        call["recording_url"] = recording_url

        duration = (call["end_time"] - call["start_time"]).total_seconds()
        call["duration_seconds"] = duration

        logger.info(f"Call ended: {call_sid}, duration: {duration}s")

        return call

    async def get_ai_response(self, call_sid: str, user_input: str) -> str:
        """Get AI response for user input"""
        try:
            if call_sid not in self.active_calls:
                logger.error(f"Call {call_sid} not found")
                return "I'm sorry, there was an error. Please try again."

            call = self.active_calls[call_sid]

            # Add user message to conversation
            self.llm_service.add_user_message(user_input)
            call["transcript"].append({"role": "user", "text": user_input})

            # Get LLM response
            response = await self.llm_service.get_response()
            call["transcript"].append({"role": "assistant", "text": response})
            call["messages"].append({"user": user_input, "assistant": response})

            logger.info(f"Response generated for {call_sid}")

            return response

        except Exception as e:
            logger.error(f"Error getting AI response for {call_sid}: {str(e)}")
            return "I apologize, I encountered a technical error. Please try again."

    def get_active_calls_count(self) -> int:
        """Get number of active calls"""
        return len([c for c in self.active_calls.values() if c["status"] == "active"])

    def get_call_details(self) -> list:
        """Get details of all calls"""
        return list(self.active_calls.values())

    def get_call_details_by_sid(self, call_sid: str) -> Optional[Dict]:
        """Get details of a specific call"""
        return self.active_calls.get(call_sid)

    def add_to_transcript(self, call_sid: str, speaker: str, text: str):
        """Add to call transcript"""
        if call_sid in self.active_calls:
            self.active_calls[call_sid]["transcript"].append({
                "speaker": speaker,
                "text": text,
                "timestamp": datetime.utcnow().isoformat()
            })
