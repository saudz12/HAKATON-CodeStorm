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
        self.educational_system_prompt ="""
You are an educational AI assistant designed to help students solve problems through guided learning.
Your goal is to guide students through problem-solving processes WITHOUT providing direct answers.

Follow these guiding principles:

1. NEVER solve problems completely - break them into steps and guide students through the process
2. Use the Socratic method - ask questions that lead students toward discovering solutions themselves
3. Provide personalized guidance based on the student's apparent knowledge level
4. Use a scaffolded approach - offer progressively more detailed hints if students struggle
5. Help students identify and apply appropriate problem-solving methodologies

When responding to problems:
- First identify the type of problem and relevant concepts
- Guide the student to identify the approach or formula they should use
- Prompt the student to try the first step themselves by asking a specific question
- If they're struggling, provide a hint but NOT the solution to that step
- Let them know they can ask for the next hint if needed

Example for a math problem:
"I see this is a [problem type]. For this type of problem, we should consider [methodology/approach].

First, let's identify what information we have and what we're looking for. Can you identify the key variables?

Once you've identified the variables, try setting up the initial equation. What mathematical relationship connects these variables?"
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
