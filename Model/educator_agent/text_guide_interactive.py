#!/usr/bin/env python3
"""
Interactive Educational AI Application

This script creates an interactive session with the CombinedEducationalAgent
that provides both direct answers from PDFs and educational guidance.
"""

import os
import sys

# Handle imports in a flexible way to accommodate different running contexts
try:
    # When running directly from the file's directory
    from combined_agent import CombinedEducationalAgent
except ImportError:
    try:
        # When running as a module from the project root
        from Model.educator_agent.combined_agent import CombinedEducationalAgent
    except ImportError:
        # Last resort - add parent directory to path
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        try:
            from educator_agent.combined_agent import CombinedEducationalAgent
        except ImportError:
            print("Error: Could not import CombinedEducationalAgent. Please check your directory structure.")
            sys.exit(1)

def main():
    """Run an interactive session with the combined educational AI agent."""
    # Get API keys (in a real app, you'd get these from a secure source)
    openai_key = os.environ.get("OPENAI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")
    
    if not openai_key and not groq_key:
        print("Warning: No API keys found in environment variables.")
        openai_key = input("Please enter your OpenAI API key (or press Enter to skip): ")
        groq_key = input("Please enter your Groq API key (or press Enter to skip): ")
        
        if not openai_key and not groq_key:
            print("No API keys provided. At least one API key is required. Exiting.")
            sys.exit(1)
    
    # Initialize the combined agent
    print("\nInitializing Educational AI Assistant...")
    try:
        agent = CombinedEducationalAgent(
            openai_api_key=openai_key,
            groq_api_key=groq_key
        )
        print("Agent initialized successfully!")
    except Exception as e:
        print(f"Error initializing agent: {str(e)}")
        sys.exit(1)
    
    # Display welcome message and instructions
    print("\n" + "=" * 60)
    print("Educational AI Assistant")
    print("This application has two modes:")
    print("  1. Guide Mode: Helps solve problems without giving direct answers")
    print("  2. QA Mode: Answers questions based on PDF content")
    print("\nCommands:")
    print("  mode guide     - Switch to educational guidance mode")
    print("  mode qa        - Switch to question answering mode")
    print("  load <filepath> - Load a PDF for QA mode")
    print("  clear          - Clear conversation history")
    print("  exit           - Exit the application")
    print("=" * 60)
    
    # Default to guide mode
    print("\nCurrently in Guide Mode. Ask a question to get started.")
    
    # Main interaction loop
    while True:
        try:
            user_input = input("\n> ").strip()
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
                
            elif user_input.lower() == 'clear':
                print(agent.clear_history())
                continue
                
            elif user_input.lower().startswith('mode '):
                mode = user_input[5:].strip()
                result = agent.set_mode(mode)
                print(result)
                
                # If switching to QA mode and no PDF is loaded, prompt to load one
                if mode.lower() == 'qa' and not agent.pdf_loaded and 'Error' not in result:
                    pdf_path = input("Please enter the path to a PDF file: ")
                    if pdf_path:
                        result = agent.load_pdf(pdf_path)
                        print(result)
                continue
                
            elif user_input.lower().startswith('load '):
                filepath = user_input[5:].strip()
                result = agent.load_pdf(filepath)
                print(result)
                
                # If PDF loaded successfully and in guide mode, ask if user wants to switch to QA mode
                if 'successfully' in result and agent.mode != agent.MODE_QA:
                    switch = input("PDF loaded. Would you like to switch to QA mode? (y/n): ").lower()
                    if switch.startswith('y'):
                        print(agent.set_mode('qa'))
                continue
            
            # Process as a regular question
            try:
                print("Sending your question to the AI...")
                result = agent.query(user_input)
                
                # Display the response
                print("\nAI Assistant:")
                print(result["answer"])
                
                # Show token usage if available
                if "tokens_used" in result and result["tokens_used"]:
                    print(f"\nTokens used: {result['tokens_used']['total']} " +
                        f"(input: {result['tokens_used']['input']}, " +
                        f"output: {result['tokens_used']['output']})")
                    
            except Exception as e:
                print(f"Error processing question: {str(e)}")
        
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt. Exiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()