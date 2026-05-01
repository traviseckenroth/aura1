from app.services.vision_encoder import vision_encoder
from app.services.memory_store import memory_store
import io

class VisualIdentityIngestor:
    def __init__(self, user_id):
        self.user_id = user_id

    def process_drive_images(self, image_streams):
        """
        Requirement #2: Extracting visual DNA from Google Drive.
        Scans personal photos to understand the user's fashion and lifestyle.
        """
        visual_traits = []
        
        for img_data in image_streams:
            # Use CLIP to get a description of the user's visual style
            # This identifies 'edgy tailoring', 'military backgrounds', etc.
            aesthetic_summary = vision_encoder.describe_visual_style(img_data)
            visual_traits.append(aesthetic_summary)
        
        # Aggregate the visual traits into a coherent 'Identity Summary'
        # e.g., "The user consistently wears relaxed, edgy tailoring and prefers urban settings."
        final_identity = self._synthesize_visual_traits(visual_traits)
        
        # Store this in the Vector DB so the Twin can use it in conversation
        memory_store.upsert_memory(
            self.user_id, 
            "visual_identity", 
            f"Visual Style Summary: {final_identity}"
        )
        print(f"[FORGE] Visual Identity integrated for {self.user_id}.")

    def _synthesize_visual_traits(self, traits):
        # Logic to find common denominators in the visual data
        # For now, it compiles them into a descriptive block for the LLM
        return " ".join(set(traits))