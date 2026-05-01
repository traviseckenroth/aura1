from app.services.vision_encoder import vision_encoder
from app.services.llm_inference import twin_engine

def evaluate_potential_match(user_a, user_b):
    """
    Requirement #4: Physical Check -> Twin Conversation -> Judge
    """
    # STEP A: Physical Gatekeeper
    # Score User B's photo against User A's trained preference vector
    visual_score = vision_encoder.compute_attraction_score(
        user_a.physical_preference_vector, 
        user_b.actual_profile_pic
    )

    if visual_score < 0.75:
        return None # Discard: Not their physical type

    # STEP B: Twin-to-Twin Arena (LLM Conversation)
    # Twin A talks to Twin B autonomously
    transcript = run_autonomous_chat(user_a.id, user_b.id)

    # STEP C: Model-Judged Potential
    # A third 'Judge' prompt evaluates if the match is high-value
    match_quality = twin_engine.evaluate_chemistry(transcript)

    if match_quality['score'] > 80:
        return {
            "profile": user_b,
            "transcript": transcript,
            "summary": match_quality['summary']
        }
    return None