from typing import Dict

class DocumentMemory:
	"""
	Simple in-memory storage for document contexts.
	"""
	def __init__(self):
		self.memory: Dict[str, str] = {}

	def store(self, doc_id: str, content: str):
		self.memory[doc_id] = content

	def get(self, doc_id: str) -> str:
		return self.memory.get(doc_id, "")

	def list_docs(self):
		return list(self.memory.keys())
