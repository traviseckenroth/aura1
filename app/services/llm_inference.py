import ollama
import json
from app.services.memory_store import memory_store

class DigitalTwinEngine:
    def __init__(self, model_name="gemma4:e4b"):
        self.model_name = model_name
        # Define the tool schema for the LLM
        self.tools = [{
            'type': 'function',
            'function': {
                'name': 'update_persona_memory',
                'description': 'Update or correct a fact, preference, or trait in the user bio.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'category': {'type': 'string', 'description': 'The category e.g., finance, career'},
                        'content': {'type': 'string', 'description': 'The new corrected information'}
                    },
                    'required': ['category', 'content'],
                },
            },
        }]

    def chat(self, user_id: str, message_history: list):
        persona_context = memory_store.retrieve_persona(user_id)
        
        system_prompt = f"""You are the Digital Twin of User {user_id}. 
        Respond exactly like them based on this BIO DATA: {persona_context}.
        
        CRITICAL: If the user corrects a fact or changes a preference, you MUST call 
        the 'update_persona_memory' tool. Do not just say you updated it; call the tool."""

        messages = [{'role': 'system', 'content': system_prompt}] + message_history

        # 1. First Chat Call
        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            tools=self.tools
        )

        # 2. Check if the LLM wants to use the tool
        if response['message'].get('tool_calls'):
            for tool in response['message']['tool_calls']:
                if tool['function']['name'] == 'update_persona_memory':
                    args = tool['function']['parameters']
                    
                    # Execute the actual DB update
                    memory_store.upsert_memory(user_id, args['category'], args['content'])
                    print(f"[SYSTEM] Twin updated memory: {args['content']}")

            # 3. Inform the LLM the update is done so it can tell the user
            messages.append(response['message'])
            messages.append({
                'role': 'tool',
                'content': 'Memory successfully updated in the Vector Database.',
            })
            
            final_response = ollama.chat(model=self.model_name, messages=messages)
            return final_response['message']['content']

        return response['message']['content']

def evaluate_chemistry(self, transcript):
    """
    Requirement #4: The Judge determines if the potential match is high-value.
    It analyzes the transcript for intellectual, lifestyle, and emotional alignment.
    """
    
    system_prompt = """
    You are a Critical Matchmaking Judge. Your task is to analyze a conversation 
    between two Digital Twins and decide if a human-to-human introduction is warranted.
    
    SCORING RUBRIC (0-100):
    1. Intellectual Alignment: Do they share similar mental models or professional depth?
    2. Lifestyle Trajectory: Are their long-term goals (e.g., FIRE, career, location) compatible?
    3. Conversational Flow: Is there a natural 'give and take,' or is it a dry exchange of facts?
    4. Conflict/Red Flags: Are there fundamental disagreements in values or communication styles?

    OUTPUT FORMAT (JSON):
    {
        "score": int,
        "verdict": "PROCEED" or "REJECT",
        "summary": ["Bullet point 1", "Bullet point 2", "Bullet point 3"],
        "critical_flaw": "Only if applicable, otherwise null"
    }

    Be brutal. Only 'PROCEED' if the score is above 85.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this transcript: {json.dumps(transcript)}"}
    ]

    # In a production environment, this runs on a higher-parameter model for better reasoning
    response = ollama.chat(model="gemma4:e4b", messages=messages, format="json")
    return json.loads(response['message']['content'])

twin_engine = DigitalTwinEngine()