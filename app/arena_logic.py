from app.services.memory_store import memory_store
from app.services.vision_encoder import vision_encoder
from app.services.llm_inference import twin_engine

def run_real_overnight_batch(user_id, user_pref_vector):
    """
    Requirement #4 & #5: 
    Finds real users, filters by visual preference, 
    then runs the LLM conversations.
    """
    final_matches = []
    
    # 1. Search Vector DB for all other users (excluding self)
    # In a real app, this queries your user database
    potential_candidates = db.get_all_users_except(user_id) 

    for candidate in potential_candidates:
        # A. PHYSICAL GATEKEEPER
        visual_score = vision_encoder.compute_attraction_score(
            user_pref_vector, 
            candidate['profile_pic']
        )
        
        if visual_score > 0.75: # Only proceed if they are "their type"
            
            # B. TWIN CONVERSATION ARENA
            transcript = simulate_twin_conversation(user_id, candidate['id'])
            
            # C. CONVERSATIONAL ATTRACTION JUDGE
            eval_data = twin_engine.evaluate_chemistry(transcript)
            
            if eval_data['score'] > 80: # Requirement #5: High Attraction Only
                final_matches.append({
                    "user": candidate,
                    "transcript": transcript,
                    "summary": eval_data['summary']
                })
                
    return final_matches