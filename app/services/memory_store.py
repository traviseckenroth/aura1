from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
import json

class PersonaMemoryStore:
    def __init__(self, collection_name="twin_personas"):
        # Local In-Memory for dev; easily points to a Dockerized Qdrant for production
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name
        
        # Initialize Local Embedding Model
        # This runs on your hardware. No data is sent to the cloud.
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        self.vector_size = 384  # matches MiniLM output size

        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

    def embed_text(self, text: str) -> list[float]:
        """Converts text to vectors locally."""
        return self.model.encode(text).tolist()

    def upsert_memory(self, user_id: str, category: str, content: str):
        """Vectorize and save a piece of the user's persona."""
        vector = self.embed_text(content)
        memory_id = str(uuid.uuid4())

        point = PointStruct(
            id=memory_id,
            vector=vector,
            payload={
                "user_id": user_id,
                "category": category,
                "content": content
            }
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def retrieve_persona(self, user_id: str, query: str = None, top_k: int = 5) -> str:
        """Fetch relevant context for the LLM system prompt."""
        if query:
            query_vector = self.embed_text(query)
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]},
                limit=top_k
            )
            return json.dumps([hit.payload['content'] for hit in results], indent=2)
        
        # Default to grabbing the most recent entries
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]},
            limit=15
        )
        return json.dumps([hit.payload['content'] for hit in results[0]], indent=2)

memory_store = PersonaMemoryStore()