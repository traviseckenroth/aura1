import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np

class VisualGatekeeper:
    def __init__(self):
        # Load the lightweight CLIP model
        self.model_name = "openai/clip-vit-base-patch32"
        self.processor = CLIPProcessor.from_pretrained(self.model_name)
        self.model = CLIPModel.from_pretrained(self.model_name)
        
    def get_image_embedding(self, image_path: str):
        """Converts an image into a 512-dimension vector."""
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        
        # Normalize the vector so we can use Cosine Similarity
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.numpy().flatten()

    def calculate_preference_centroid(self, liked_image_paths: list):
        """
        Takes all the images a user 'liked' during onboarding 
        and creates a single average vector representing their 'type'.
        """
        embeddings = [self.get_image_embedding(img) for img in liked_image_paths]
        centroid = np.mean(embeddings, axis=0)
        # Normalize the centroid
        return centroid / np.linalg.norm(centroid)

    def compute_attraction_score(self, user_preference_vector, target_profile_image_path):
        """
        Scores a real profile image against the user's preference.
        Returns a score between 0 and 1.
        """
        target_vector = self.get_image_embedding(target_profile_image_path)
        # Cosine similarity
        score = np.dot(user_preference_vector, target_vector)
        return float(score)

# Singleton instance
vision_encoder = VisualGatekeeper()