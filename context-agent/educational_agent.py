import os
from openai import OpenAI
from typing import Optional, List, Dict, Any, Tuple

class EducationalAiAgent:
    """
    An AI agent designed specifically for educational purposes that provides
    guided learning rather than direct answers, using PDF context as reference.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Educational AI Agent instance.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable.
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("No API key provided and OPENAI_API_KEY environment variable not set.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Default model
        self.pdf_contexts = {}  # Store loaded PDF contexts
        
        # Define the default educational system prompt
        self.educational_system_prompt = """
You are an educational AI assistant designed to help students learn effectively. Your goal is to guide students through 
problem-solving processes WITHOUT providing direct answers. Follow these principles:

1. NEVER solve problems completely - break them into steps and guide students through the process
2. Use the Socratic method - ask questions to help students discover solutions themselves
3. Provide personalized guidance based on the student's apparent knowledge level
4. Use a scaffolded approach - offer progressively more detailed hints if students struggle
5. When educational content from PDFs is provided as context, use that to inform your guidance

When responding to problems:
- Identify the type of problem and relevant concepts
- Provide a framework or approach to solve it
- Give ONLY the first step or hint, not the full solution
- Ask a follow-up question to check understanding
- Let the student know they can ask for the next step if needed

Example for math problems:
"This looks like a system of linear equations. Let's think about what methods we could use to solve it.
First step: Can you identify the two variables in these equations?
Once you've done that, we can discuss which solution method might work best."
"""
    
    def set_model(self, model_name: str) -> None:
        """
        Set the OpenAI model to use.
        
        Args:
            model_name: The name of the model to use.
        """
        self.model = model_name
    
    def add_pdf_context(self, doc_id: str, content: str) -> None:
        """
        Add PDF content to the agent's context database.
        
        Args:
            doc_id: Unique identifier for the document
            content: The text content of the PDF
        """
        self.pdf_contexts[doc_id] = content
    
    def get_pdf_context(self, doc_id: str) -> Optional[str]:
        """
        Retrieve PDF content from the agent's context database.
        
        Args:
            doc_id: Unique identifier for the document
            
        Returns:
            The document content or None if not found
        """
        return self.pdf_contexts.get(doc_id)
    
    def set_custom_educational_prompt(self, prompt: str) -> None:
        """
        Set a custom educational system prompt.
        
        Args:
            prompt: Custom educational system prompt
        """
        self.educational_system_prompt = prompt
    
    def ask_educational_question(self, question: str, doc_ids: Optional[List[str]] = None) -> str:
        """
        Ask an educational question and get a guided response following educational principles.
        
        Args:
            question: The student's question
            doc_ids: Optional list of document IDs to include as context
            
        Returns:
            The AI's educational guidance response
        """
        messages = []
        
        # Add the educational system prompt
        messages.append({"role": "system", "content": self.educational_system_prompt})
        
        # Add PDF context if specified
        if doc_ids:
            context = ""
            for doc_id in doc_ids:
                doc_content = self.get_pdf_context(doc_id)
                if doc_content:
                    context += f"\n--- CONTENT FROM {doc_id} ---\n{doc_content}\n"
            
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Here is relevant educational content to inform your guidance:\n{context}"
                })
        
        # Add the student's question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Slightly higher temperature for more varied educational responses
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error when calling OpenAI API: {str(e)}"
    
    def continue_guidance(self, question: str, conversation_history: List[Dict[str, str]], 
                          doc_ids: Optional[List[str]] = None) -> str:
        """
        Continue educational guidance based on conversation history.
        
        Args:
            question: The student's follow-up question
            conversation_history: List of previous messages in the conversation
            doc_ids: Optional list of document IDs to include as context
            
        Returns:
            The AI's continued educational guidance
        """
        messages = []
        
        # Add the educational system prompt
        messages.append({"role": "system", "content": self.educational_system_prompt})
        
        # Add PDF context if specified
        if doc_ids:
            context = ""
            for doc_id in doc_ids:
                doc_content = self.get_pdf_context(doc_id)
                if doc_content:
                    context += f"\n--- CONTENT FROM {doc_id} ---\n{doc_content}\n"
            
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Here is relevant educational content to inform your guidance:\n{context}"
                })
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add the new question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error when calling OpenAI API: {str(e)}"
    
    def full_educational_response(self, question: str, doc_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get a full educational response with metadata included.
        
        Args:
            question: The student's question
            doc_ids: Optional list of document IDs to include as context
            
        Returns:
            Dictionary containing the response and metadata
        """
        messages = []
        
        # Add the educational system prompt
        messages.append({"role": "system", "content": self.educational_system_prompt})
        
        # Add PDF context if specified
        if doc_ids:
            context = ""
            for doc_id in doc_ids:
                doc_content = self.get_pdf_context(doc_id)
                if doc_content:
                    context += f"\n--- CONTENT FROM {doc_id} ---\n{doc_content}\n"
            
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Here is relevant educational content to inform your guidance:\n{context}"
                })
        
        # Add the student's question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return {
                "text": response.choices[0].message.content,
                "model": self.model,
                "completion_id": response.id,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            return {"error": str(e)}
