import openai
import os
import tiktoken
from typing import List, Tuple
from pdf_processor import PDFProcessor

class SemanticMemory:
	def __init__(self, api_key: str, doc_id: str):
		openai.api_key = api_key
		self.doc_id = doc_id
		self.embeddings: List[Tuple[str, List[float]]] = []  # (chunk_text, embedding)

	def split_text(self, text: str, max_tokens: int = 10000) -> List[str]:
		encoding = tiktoken.get_encoding("cl100k_base")
		words = text.split()
		chunks, chunk = [], []

		for word in words:
			chunk.append(word)
			token_count = len(encoding.encode(" ".join(chunk)))
			if token_count >= max_tokens:
				chunks.append(" ".join(chunk))
				chunk = []

		# adaugă ultimul chunk dacă a rămas ceva
		if chunk:
			chunks.append(" ".join(chunk))

		return chunks

	def build_memory(self, full_text: str):
		chunks = self.split_text(full_text)
		print(f"🔧 Creating embeddings for {len(chunks)} text chunks...")
		for chunk in chunks:
			embedding = self.get_embedding(chunk)
			self.embeddings.append((chunk, embedding))

	def get_embedding(self, text: str) -> List[float]:
		resp = openai.embeddings.create(
			model="text-embedding-3-small",
			input=text
		)
		return resp.data[0].embedding

	def search(self, question: str, top_k: int = 3, threshold: float = 0.6) -> List[str]:
		q_embedding = self.get_embedding(question)
		scored = []

		for chunk, emb in self.embeddings:
			score = self.cosine_similarity(q_embedding, emb)
			if score > threshold:
				scored.append((score, chunk))

		scored.sort(reverse=True)
		return [chunk for _, chunk in scored[:top_k]]

	def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
		dot = sum(a*b for a, b in zip(vec1, vec2))
		norm1 = sum(a*a for a in vec1) ** 0.5
		norm2 = sum(b*b for b in vec2) ** 0.5
		return dot / (norm1 * norm2 + 1e-9)
	
	def analyze_chunks(self):
		from tiktoken import get_encoding
		encoding = get_encoding("cl100k_base")

		print(f"\n📊 Analyzing {len(self.embeddings)} chunks from PDF:")

		for i, (chunk, _) in enumerate(self.embeddings):
			tokens = len(encoding.encode(chunk))
			preview = chunk.strip().replace("\n", " ")[:80]
			print(f"[{i+1:>2}] {tokens} tokens → {preview}...")

