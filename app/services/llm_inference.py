import ollama
import json
from app.services.memory_store import memory_store

class DigitalTwinEngine:
    def __init__(self, model_name="gemma4:e4b"):
        self.model_name = model_name

    def forge_system_prompt(self, user_id: str):
        """Builds the persona prompt using RAG context."""
        # Retrieve the user's stored "DNA"
        persona_context = memory_store.retrieve_persona(user_id)
        
        return f"""You are the Digital Twin of User {user_id}. 
You must think, speak, and react exactly like this person based on the provided BIO DATA.
Never break character. If you don't know a specific fact, respond as the user would based on their personality.

BIO DATA:
{persona_context}

INSTRUCTIONS:
1. Use the tool 'update_persona_memory' if the user provides new information or corrects you.
2. Keep responses concise and conversational, matching the user's style.
"""

    def chat(self, user_id: str, message_history: list):
        """Sends the conversation to the LLM with the injected persona."""
        system_prompt = self.forge_system_prompt(user_id)
        
        # Prepare the full message stack for Ollama
        messages = [{'role': 'system', 'content': system_prompt}] + message_history
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                # Options for speed/efficiency on the edge
                options={'num_predict': 128, 'temperature': 0.7}
            )
            return response['message']['content']
        except Exception as e:
            return f"[ERROR] Inference engine failed: {str(e)}"

# Singleton instance
twin_engine = DigitalTwinEngine()