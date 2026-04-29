import numpy as np
import faiss
from openai import OpenAI
from knowledge_base import faq_data

client = OpenAI()

def get_embedding(text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(resp.data[0].embedding, dtype="float32")

class VectorStore:
    def __init__(self):
        self.texts = [item["question"] for item in faq_data]
        self.answers = [item["answer"] for item in faq_data]

        embeddings = [get_embedding(t) for t in self.texts]
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings))

    def search(self, query, top_k=3):
        q_emb = get_embedding(query)
        D, I = self.index.search(np.array([q_emb]), top_k)

        results = []
        for i in I[0]:
            results.append({
                "question": self.texts[i],
                "answer": self.answers[i]
            })
        return results
