from celery import Celery
import json
from app.services.memory_store import memory_store
from app.services.llm_inference import twin_engine
from app.services.vision_encoder import vision_encoder
from app.workers.celery_app import celery_instance
from app.services.llm_inference import twin_engine
from app.services.vision_encoder import vision_encoder
import json

# Initialize Celery
celery_app = Celery('match_tasks', broker='redis://localhost:6379/0')

class MatchmakingArena:
    def __init__(self, model_name="gemma4:e4b"):
        self.model_name = model_name

    def simulate_conversation(self, user_a_id, user_b_id, turns=3):
        """Runs an autonomous conversation between two digital twins."""
        conversation = []
        
        # Initial greeting from Twin A to Twin B
        current_prompt = "You are starting a conversation with someone your visual filters liked. Write a brief, engaging opening message based on your persona."
        
        for i in range(turns * 2):
            # Alternate between User A and User B
            current_user = user_a_id if i % 2 == 0 else user_b_id
            other_user = user_b_id if i % 2 == 0 else user_a_id
            role = "Twin A" if i % 2 == 0 else "Twin B"

            # Generate response from the current twin
            response = twin_engine.chat(current_user, conversation)
            conversation.append({"role": "assistant", "content": f"{role}: {response}"})
            
        return conversation

    def evaluate_match(self, transcript):
        """Uses the LLM as a judge to score the conversation."""
        evaluator_prompt = [
            {"role": "system", "content": "You are an expert relationship psychologist. Analyze the following conversation between two digital twins. Score their compatibility from 1-100 and provide 3 brief bullet points on why."},
            {"role": "user", "content": f"TRANSCRIPT:\n{json.dumps(transcript)}"}
        ]
        
        # Use the twin_engine logic to get an evaluation
        raw_eval = twin_engine.chat("evaluator_system", evaluator_prompt)
        return raw_eval

@celery_app.task
def run_overnight_batch(user_id):
    print(f"[ARENA] Initiating overnight simulations for {user_id}...")
    """The main task triggered by the overnight scheduler."""
    arena = MatchmakingArena()
    matches = []

    # 1. PRE-SCREEN: Find 5 candidates who pass the Visual Gatekeeper
    # (In production, this queries the DB for all active users of preferred sex)
    candidates = ["user_002", "user_003", "user_004"] 
    
    user_a_pref_vector = [0.1] * 512 # Placeholder for the user's preference vector

    for candidate_id in candidates:
        candidate_pic = f"data/profiles/{candidate_id}.jpg"
        
        # Requirement #4: Check physical attraction first
        if vision_encoder.compute_attraction_score(user_a_pref_vector, candidate_pic) > 0.7:
            
            # Requirement #1: Conduct LLM-to-LLM conversation
            transcript = arena.simulate_conversation(user_id, candidate_id)
            
            # Requirement #4: Judge the match
            evaluation = arena.evaluate_match(transcript)
            
            matches.append({
                "match_id": candidate_id,
                "transcript": transcript,
                "evaluation": evaluation
            })

    # Save the top matches to the 'twin_simulations' table for the morning drop
    # save_to_db(user_id, matches)
    print(f"[ARENA] Overnight batch complete for {user_id}. Found {len(matches)} high-quality matches.")