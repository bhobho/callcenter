import os
from anthropic import Anthropic

class LLMService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []

    def set_system_prompt(self, system_prompt: str):
        """Set the system prompt for the call center agent"""
        self.system_prompt = system_prompt

    def add_user_message(self, message: str):
        """Add a user message to conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

    def get_response(self) -> str:
        """
        Get LLM response based on conversation history

        Returns:
            Agent's response text
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message
        except Exception as e:
            print(f"LLM error: {e}")
            raise

    def reset_conversation(self):
        """Reset conversation history for a new call"""
        self.conversation_history = []

    def get_conversation_context(self) -> list:
        """Get the current conversation history"""
        return self.conversation_history.copy()
