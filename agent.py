import os
from openai import OpenAI
from typing import Optional, List, Dict, Any

class AiResponse:
    """
    A class to interact with OpenAI's API for generating responses to questions.
    Basic implementation for testing API key functionality.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AiResponse instance.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable.
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("No API key provided and OPENAI_API_KEY environment variable not set.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Default model
    
    def set_model(self, model_name: str) -> None:
        """
        Set the OpenAI model to use.
        
        Args:
            model_name: The name of the model to use.
        """
        self.model = model_name
    
    def ask_question(self, question: str, system_prompt: Optional[str] = None) -> str:
        """
        Ask a question to the AI and get a response.
        
        Args:
            question: The question to ask.
            system_prompt: Optional system prompt to guide the AI's behavior.
            
        Returns:
            The AI's response as a string.
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add user question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error when calling OpenAI API: {str(e)}"
    
    def ask_with_context(self, question: str, context: str, system_prompt: Optional[str] = None) -> str:
        """
        Ask a question with additional context and get a response.
        
        Args:
            question: The question to ask.
            context: Additional context to provide to the AI.
            system_prompt: Optional system prompt to guide the AI's behavior.
            
        Returns:
            The AI's response as a string.
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add context as a system message
        messages.append({"role": "system", "content": f"Here is some context: {context}"})
        
        # Add user question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error when calling OpenAI API: {str(e)}"


# Example usage
if __name__ == "__main__":
    # You can set your API key here for testing, or use an environment variable
    # api_key = "your-api-key-here"
    
    # Create an instance of AiResponse
    ai = AiResponse(api_key='insert key here')  # Will use OPENAI_API_KEY environment variable
    
    # Ask a simple question to test the API key
    question = "What is the capital of France?"
    print(f"Question: {question}")
    print(f"Response: {ai.ask_question(question)}")