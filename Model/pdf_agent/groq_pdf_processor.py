import os
from pypdf import PdfReader
import numpy as np
from sentence_transformers import SentenceTransformer
import groq
from typing import List, Dict, Tuple

class PDFContextQA:
    def __init__(self, api_key: str, model_name: str = "llama3-70b-8192"):
        """
        Initialize the PDF Context QA system
        
        Args:
            api_key: Groq API key
            model_name: Model to use for Q&A
        """
        self.groq_client = groq.Groq(api_key=api_key)
        self.model_name = model_name
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Storage for document chunks and their embeddings
        self.chunks = []
        self.chunk_embeddings = []
        
    def load_pdf(self, pdf_path: str, chunk_size: int = 1000, overlap: int = 200):
        """
        Load PDF content and split into chunks
        
        Args:
            pdf_path: Path to the PDF file
            chunk_size: Size of chunks in characters
            overlap: Overlap between chunks in characters
        """
        # Extract text from PDF
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Split text into chunks with overlap
        self.chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk) >= 200:  # Only keep chunks of sufficient size
                self.chunks.append(chunk)
        
        # Generate embeddings for chunks
        self.chunk_embeddings = self.embedding_model.encode(self.chunks)
        print(f"Loaded {len(self.chunks)} chunks from PDF")
        
    def get_relevant_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve most relevant chunks for a query
        
        Args:
            query: User question
            top_k: Number of top chunks to retrieve
            
        Returns:
            List of most relevant text chunks
        """
        # Create embedding for the query
        query_embedding = self.embedding_model.encode(query)
        
        # Calculate similarity scores
        similarities = np.dot(self.chunk_embeddings, query_embedding)
        
        # Get indices of top_k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return top chunks
        return [self.chunks[i] for i in top_indices]
    
    def answer_question(self, query: str) -> Dict:
        """
        Answer question based on PDF context
        
        Args:
            query: User question
            
        Returns:
            Dict containing answer and token usage info
        """
        # Get relevant context chunks
        relevant_chunks = self.get_relevant_chunks(query)
        context = "\n\n".join(relevant_chunks)
        
        # Create system prompt with context
        system_prompt = f"""You are a helpful assistant that answers questions based on the provided context.
        
CONTEXT:
{context}

Answer the question based ONLY on the information provided in the context. If the answer cannot be found in the context, say "I don't have enough information to answer this question." Do not make up information."""
        
        # Send request to Groq
        response = self.groq_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        
        # Return answer and token usage
        return {
            "answer": response.choices[0].message.content,
            "tokens_used": {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens,
                "total": response.usage.total_tokens
            }
        }

# Example usage
if __name__ == "__main__":
    # Initialize with your API key
    #api_key = os.environ.get("GROQ_API_KEY", "api-key")
    api_key = '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'
    qa_system = PDFContextQA(api_key)
    
    # Load PDF
    qa_system.load_pdf("C:\\Users\\Saud Shaikh\\Downloads\\sodapdf-converted.pdf")
    
    # Ask questions
    while True:
        question = input("\nAsk a question (or type 'exit' to quit): ")
        if question.lower() == "exit":
            break
            
        result = qa_system.answer_question(question)
        print(f"\nAnswer: {result['answer']}")
        print(f"\nTokens used: {result['tokens_used']['total']} " +
              f"(input: {result['tokens_used']['input']}, " +
              f"output: {result['tokens_used']['output']})")