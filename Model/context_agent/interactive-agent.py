#!/usr/bin/env python3
"""
Interactive Educational AI Agent

This script creates an interactive session with the EducationalAiAgent
where you can ask multiple questions in sequence and maintain conversation context.
"""

import os
from educational_agent import EducationalAiAgent 

def main():
    """
    Run an interactive session with the educational AI agent.
    """
    # Initialize the Educational AI Agent
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    agent = EducationalAiAgent()
    
    # Optional: Set a different model if needed
    # agent.set_model("gpt-4-turbo")
    
    print("\n" + "=" * 60)
    print("Educational AI Assistant")
    print("Ask questions to get guided learning assistance. Type 'exit' to quit.")
    print("=" * 60)
     
    # Keep track of the conversation history
    conversation_history = []
    
    while True:
        # Get student questionit
        question = input("\nYour question: ")
        
        if question.lower() in ['exit', 'quit', 'q']:
            break
        
        # Get educational guidance
        if not conversation_history:
            # First question in the conversation
            response = agent.ask_educational_question(question)
        else:
            # Continue the conversation with history
            response = agent.continue_guidance(question, conversation_history)
     
        # Display the response
        print("\nAI Assistant:")
        print(response)
        
        # Update conversation history for context in the next iteration
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": response})
         
if __name__ == "__main__":
    main()
