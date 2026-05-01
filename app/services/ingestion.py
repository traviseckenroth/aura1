import whisper
from app.services.memory_store import memory_store

def forge_persona(user_id, bio_text=None, media_path=None, drive_files=None):
    """
    Requirement #2: Capture text, audio, video, and Drive repos.
    """
    # 1. Text Bio
    if bio_text:
        memory_store.upsert_memory(user_id, "bio_text", bio_text)

    # 2. Audio/Video Bio (Whisper Transcription)
    if media_path:
        model = whisper.load_model("base")
        transcript = model.transcribe(media_path)["text"]
        memory_store.upsert_memory(user_id, "vocal_bio", transcript)

    # 3. Google Drive Deep-Dive (Texts/Chat Logs)
    if drive_files:
        # drive_files would be a list of strings extracted via Google API
        combined_logs = " ".join(drive_files)
        memory_store.upsert_memory(user_id, "historical_data", combined_logs)
    
    print(f"[SYSTEM] Digital Twin for {user_id} is now forged.")