import os
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        self.system_prompt = ""

    def set_system_prompt(self, system_prompt: str):
        """Set the system prompt for the call center agent"""
        self.system_prompt = system_prompt
        logger.info("System prompt set for LLM service")

    def add_user_message(self, message: str):
        """Add a user message to conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

    def get_response(self) -> str:
        """
        Get LLM response based on conversation history with streaming support

        Returns:
            Agent's response text
        """
        try:
            if not self.system_prompt:
                raise ValueError("System prompt not set")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text

            # Ensure response is concise for voice interaction
            if len(assistant_message) > 500:
                assistant_message = assistant_message[:500] + "..."

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            logger.debug(f"LLM response: {assistant_message[:100]}...")

            return assistant_message

        except Exception as e:
            logger.error(f"LLM error: {e}")
            raise

    def reset_conversation(self):
        """Reset conversation history for a new call"""
        self.conversation_history = []
        logger.info("Conversation history reset")

    def get_conversation_context(self) -> list:
        """Get the current conversation history"""
        return self.conversation_history.copy()

    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation yet"

        summary = f"Conversation with {len(self.conversation_history)} messages:\n"
        for i, msg in enumerate(self.conversation_history, 1):
            role = msg["role"].upper()
            content = msg["content"][:100]
            summary += f"{i}. {role}: {content}\n"

        return summary
