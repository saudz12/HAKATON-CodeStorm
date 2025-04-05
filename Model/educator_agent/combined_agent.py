#!/usr/bin/env python3
"""
Improved Combined Educational Agent

This application integrates two specialized AI agents:
1. EducationalAiAgent: Helps solve problems without direct answers (OpenAI)
2. PDFContextQA: Answers questions based on PDF content (Groq)

With fixed mode switching to ensure prompts go to the correct model.
"""

import os
from typing import Optional, List, Dict, Any, Tuple

# Import the specialized agents - modify these imports based on your project structure
# For absolute imports (when running as a module):
# from Model.context_agent.educational_agent import EducationalAiAgent
# from Model.pdf_agent.groq_pdf_processor import PDFContextQA

# For local imports (when running directly):
try:
    # Try local imports first
    from context_agent.educational_agent import EducationalAiAgent
    from pdf_agent.groq_pdf_processor import PDFContextQA
except ImportError:
    try:
        # Try absolute imports if local imports fail
        from Model.context_agent.educational_agent import EducationalAiAgent
        from Model.pdf_agent.groq_pdf_processor import PDFContextQA
    except ImportError:
        # Try relative imports as a last resort
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from Model.context_agent.educational_agent import EducationalAiAgent
        from Model.pdf_agent.groq_pdf_processor import PDFContextQA

class CombinedEducationalAgent:
    """
    Educational agent that integrates guide mode and QA mode by using
    specialized agent classes with fixed mode handling.
    """
    
    MODE_QA = "qa"  # Direct question answering mode
    MODE_GUIDE = "guide"  # Educational guidance mode
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None,
        openai_model: str = "gpt-3.5-turbo",
        groq_model: str = "llama3-70b-8192"
    ):
        """Initialize the agent with API keys and create specialized agent instances."""
        # Initialize OpenAI-based Educational Agent
        self.guide_agent = None
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        
        if openai_api_key:
            try:
                self.guide_agent = EducationalAiAgent(api_key=openai_api_key)
                self.guide_agent.set_model(openai_model)
                print("Guide agent initialized successfully with OpenAI.")
            except Exception as e:
                print(f"Warning: Failed to initialize guide agent: {str(e)}")
            
        # Initialize Groq-based PDF QA Agent
        self.qa_agent = None
        self.groq_api_key = groq_api_key
        self.groq_model = groq_model
        
        if groq_api_key:
            try:
                self.qa_agent = PDFContextQA(api_key=groq_api_key, model_name=groq_model)
                print("QA agent initialized successfully with Groq.")
            except Exception as e:
                print(f"Warning: Failed to initialize QA agent: {str(e)}")
            
        # Current operating mode
        self.mode = self.MODE_GUIDE  # Default to guide mode
        
        # PDF status
        self.pdf_loaded = False
        self.pdf_path = None
        
        # Conversation history format: [{"role": "user/assistant", "content": "text", "mode": "guide/qa"}]
        self.conversation_history = []
    
    def _ensure_guide_agent(self):
        """Make sure the guide agent is initialized."""
        if not self.guide_agent and self.openai_api_key:
            try:
                self.guide_agent = EducationalAiAgent(api_key=self.openai_api_key)
                self.guide_agent.set_model(self.openai_model)
                print("Guide agent initialized.")
            except Exception as e:
                print(f"Error initializing guide agent: {str(e)}")
                
    def _ensure_qa_agent(self):
        """Make sure the QA agent is initialized."""
        if not self.qa_agent and self.groq_api_key:
            try:
                self.qa_agent = PDFContextQA(api_key=self.groq_api_key, model_name=self.groq_model)
                print("QA agent initialized.")
            except Exception as e:
                print(f"Error initializing QA agent: {str(e)}")
    
    def set_mode(self, mode: str) -> str:
        """
        Set the agent's mode to either QA or guide.
        
        Args:
            mode: Either MODE_QA for direct answers or MODE_GUIDE for educational guidance
            
        Returns:
            Status message
        """
        if mode.lower() not in [self.MODE_QA, self.MODE_GUIDE]:
            return f"Invalid mode. Choose either '{self.MODE_QA}' for direct answers or '{self.MODE_GUIDE}' for educational guidance."
        
        # Ensure the appropriate agent is initialized
        if mode.lower() == self.MODE_QA:
            self._ensure_qa_agent()
            if not self.qa_agent:
                return "Error: QA mode requires a Groq API key, which is not available or invalid."
        else:  # MODE_GUIDE
            self._ensure_guide_agent()
            if not self.guide_agent:
                return "Error: Guide mode requires an OpenAI API key, which is not available or invalid."
        
        # If switching to QA mode, check if PDF is loaded
        if mode.lower() == self.MODE_QA and not self.pdf_loaded:
            return "QA mode requires a PDF to be loaded first. Please load a PDF using the load_pdf method."

        # Clear conversation history if changing modes
        mode_change_message = ""
        if self.mode != mode.lower():
            if self.conversation_history:
                self.clear_history()
                mode_change_message = f"Mode set to {mode.capitalize()}. Conversation history cleared."
            else:
                mode_change_message = f"Mode set to {mode.capitalize()}."
            
            # Set the new mode
            self.mode = mode.lower()
        else:
            mode_change_message = f"Already in {mode.capitalize()} mode."
        
        # Return appropriate confirmation message
        if self.mode == self.MODE_QA:
            return f"{mode_change_message} I will provide direct answers based on the PDF content."
        else:
            return f"{mode_change_message} I will guide you through learning without providing direct answers."
    
    def load_pdf(self, pdf_path: str, chunk_size: int = 1000, overlap: int = 200) -> str:
        """
        Load a PDF for question answering.
        
        Args:
            pdf_path: Path to the PDF file
            chunk_size: Size of chunks in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            Status message
        """
        # Ensure QA agent is initialized
        self._ensure_qa_agent()
        
        if not self.qa_agent:
            return "Error: Loading PDFs requires a Groq API key, which is not available or invalid."
        
        try:
            # Use the PDFContextQA agent's load_pdf method
            self.qa_agent.load_pdf(pdf_path, chunk_size, overlap)
            
            # Update PDF status
            self.pdf_loaded = True
            self.pdf_path = pdf_path
            
            return f"PDF loaded successfully: {pdf_path}. {len(self.qa_agent.chunks)} chunks created."
            
        except Exception as e:
            return f"Error loading PDF: {str(e)}"
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a query based on the current mode.
        
        Args:
            question: The user's question
            
        Returns:
            Dictionary with the response and metadata
        """
        # Log which mode we're using for debugging
        print(f"Current mode before processing: {self.mode}")
        print(f"Processing query in {self.mode.upper()} mode")
        
        # Add the question to conversation history
        self.conversation_history.append({
            "role": "user", 
            "content": question,
            "mode": self.mode
        })

        if self.mode == self.MODE_QA:
            return self._handle_qa_query(question)
        else:  # MODE_GUIDE
            return self._handle_guide_query(question)
    
    def _handle_qa_query(self, question: str) -> Dict[str, Any]:
        """Handle a query in QA mode."""
        # Ensure QA agent is initialized
        self._ensure_qa_agent()
        
        try:
            # Ensure PDF is loaded for QA mode
            if not self.pdf_loaded:
                result = {
                    "answer": "Please load a PDF document first using the load_pdf method.",
                    "mode": self.mode
                }
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": result["answer"],
                    "mode": self.mode
                })
                return result
            
            # Direct Q&A mode using PDFContextQA agent
            if not self.qa_agent:
                result = {
                    "answer": "QA mode is not available. Groq API key may be missing or invalid.",
                    "mode": self.mode
                }
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": result["answer"],
                    "mode": self.mode
                })
                return result
            
            # Get answer from the PDFContextQA agent
            print("Querying PDFContextQA agent...")
            qa_result = self.qa_agent.answer_question(question)
            
            result = {
                "answer": qa_result["answer"],
                "mode": self.mode,
                "tokens_used": qa_result["tokens_used"] if "tokens_used" in qa_result else None
            }
            
            # Add the answer to conversation history
            self.conversation_history.append({
                "role": "assistant", 
                "content": result["answer"],
                "mode": self.mode
            })
            
            return result
            
        except Exception as e:
            error_msg = f"Error in QA mode: {str(e)}"
            print(error_msg)
            result = {
                "answer": f"There was an error processing your question in QA mode: {str(e)}",
                "mode": self.mode
            }
            self.conversation_history.append({
                "role": "assistant", 
                "content": result["answer"],
                "mode": self.mode
            })
            return result
    
    def _handle_guide_query(self, question: str) -> Dict[str, Any]:
        """Handle a query in Guide mode."""
        # Ensure guide agent is initialized
        self._ensure_guide_agent()
        
        try:
            # Educational guidance mode using EducationalAiAgent
            if not self.guide_agent:
                result = {
                    "answer": "Educational guidance mode is not available. OpenAI API key may be missing or invalid.",
                    "mode": self.mode
                }
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": result["answer"],
                    "mode": self.mode
                })
                return result
            
            # Extract the last few conversation exchanges for context (excluding the current question)
            recent_history = []
            if len(self.conversation_history) > 1:
                # Get up to 5 recent exchanges (10 messages)
                for i in range(max(0, len(self.conversation_history) - 11), len(self.conversation_history) - 1):
                    msg = self.conversation_history[i]
                    # Only include messages from the current mode
                    if "mode" in msg and msg["mode"] == self.mode:
                        recent_history.append({"role": msg["role"], "content": msg["content"]})
            
            # Get the response from EducationalAiAgent
            print("Querying EducationalAiAgent...")
            if recent_history:
                # Continue with conversation history
                print(f"Using conversation history with {len(recent_history)} messages")
                answer = self.guide_agent.continue_guidance(question, recent_history)
            else:
                # Start a new conversation
                print("Starting new conversation")
                answer = self.guide_agent.ask_educational_question(question)
            
            result = {
                "answer": answer,
                "mode": self.mode
            }
            
            # Add the response to conversation history
            self.conversation_history.append({
                "role": "assistant", 
                "content": result["answer"],
                "mode": self.mode
            })
            
            return result
            
        except Exception as e:
            error_msg = f"Error in guide mode: {str(e)}"
            print(error_msg)
            result = {
                "answer": f"There was an error processing your question in guide mode: {str(e)}",
                "mode": self.mode
            }
            self.conversation_history.append({
                "role": "assistant", 
                "content": result["answer"],
                "mode": self.mode
            })
            return result
    
    def clear_history(self) -> str:
        """
        Clear the conversation history.
        
        Returns:
            Confirmation message
        """
        self.conversation_history = []
        return "Conversation history cleared."