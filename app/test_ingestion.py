from app.services.memory_store import memory_store

# Simulate data harvested from User A's bio/Drive
user_id_1 = "travis_001"
memories = [
    {"cat": "career", "text": "14 years in Solution Architecture and Technical Program Management."},
    {"cat": "finance", "text": "Passionate about FIRE; goal is retirement by age 48."},
    {"cat": "hobbies", "text": "Builds autonomous trading bots in Python for Bitcoin."}
]

for m in memories:
    memory_store.upsert_memory(user_id_1, m['cat'], m['text'])

# Test retrieval (what the LLM will see during a chat)
context = memory_store.retrieve_persona(user_id_1, query="What are his financial goals?")
print(f"Retrieved Context:\n{context}")