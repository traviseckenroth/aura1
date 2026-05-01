from app.services.vision_encoder import vision_encoder

class VisualTrainer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.liked_image_embeddings = []

    def process_swipe(self, image_path, is_liked):
        """
        Requirement #3: Training on system-presented images 
        to understand physical preference.
        """
        if is_liked:
            embedding = vision_encoder.get_image_embedding(image_path)
            self.liked_image_embeddings.append(embedding)

    def finalize_preference(self):
        """Generates the mathematical 'Type' of the user."""
        import numpy as np
        centroid = np.mean(self.liked_image_embeddings, axis=0)
        # Store this vector in the user's profile for the Gatekeeper
        return centroid / np.linalg.norm(centroid)