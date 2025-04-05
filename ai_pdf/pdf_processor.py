import fitz  # PyMuPDF
import os
from typing import Dict, List, Optional, Tuple, Any
import json

class PDFProcessor:
    """
    A class for processing PDF documents and extracting their contents.
    """
    
    def __init__(self, storage_dir: str = "pdf_storage"):
        """
        Initialize the PDF processor.
        
        Args:
            storage_dir: Directory to store extracted PDF content.
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def process_pdf(self, pdf_path: str, doc_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a PDF file and extract its contents.
        
        Args:
            pdf_path: Path to the PDF file.
            doc_id: Optional document ID. If not provided, the filename will be used.
            
        Returns:
            A dictionary containing the document metadata and extracted text.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Use filename as document ID if not provided
        if doc_id is None:
            doc_id = os.path.basename(pdf_path).replace('.pdf', '')
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Extract document metadata
        metadata = {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "subject": doc.metadata.get("subject", ""),
            "keywords": doc.metadata.get("keywords", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
            "page_count": len(doc),
            "doc_id": doc_id
        }
        
        # Extract text and structure from each page
        pages = []
        toc = doc.get_toc()
        
        for page_num, page in enumerate(doc):
            # Extract text
            text = page.get_text()
            
            # Extract images (optional)
            # images = self._extract_images(page)
            
            # Extract tables (requires additional processing)
            # tables = self._extract_tables(page)
            
            # Add page data
            pages.append({
                "page_num": page_num + 1,
                "text": text,
                # "images": images,
                # "tables": tables
            })
        
        # Create the document data structure
        document_data = {
            "metadata": metadata,
            "toc": toc,
            "pages": pages
        }
        
        # Save the extracted content
        self._save_document_data(doc_id, document_data)
        
        # Close the document
        doc.close()
        
        return document_data
    
    def get_document_content(self, doc_id: str) -> Dict[str, Any]:
        """
        Get the contents of a processed document.
        
        Args:
            doc_id: The document ID.
            
        Returns:
            The document data.
        """
        json_path = os.path.join(self.storage_dir, f"{doc_id}.json")
        
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Document data not found: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_document_text(self, doc_id: str) -> str:
        """
        Get the full text content of a document.
        
        Args:
            doc_id: The document ID.
            
        Returns:
            The document text.
        """
        doc_data = self.get_document_content(doc_id)
        
        # Concatenate text from all pages
        full_text = "\n\n".join(page["text"] for page in doc_data["pages"])
        
        return full_text
    
    def _save_document_data(self, doc_id: str, data: Dict[str, Any]) -> None:
        """
        Save document data to disk.
        
        Args:
            doc_id: The document ID.
            data: The document data to save.
        """
        json_path = os.path.join(self.storage_dir, f"{doc_id}.json")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def list_documents(self) -> List[str]:
        """
        List all processed documents.
        
        Returns:
            A list of document IDs.
        """
        documents = []
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                doc_id = filename.replace('.json', '')
                documents.append(doc_id)
        
        return documents
    
    def get_document_summary(self, doc_id: str) -> Dict[str, Any]:
        """
        Get a summary of document metadata.
        
        Args:
            doc_id: The document ID.
            
        Returns:
            Document metadata.
        """
        doc_data = self.get_document_content(doc_id)
        return doc_data["metadata"]
    
    def search_document(self, doc_id: str, query: str) -> List[Dict[str, Any]]:
        """
        Search for text within a document.
        
        Args:
            doc_id: The document ID.
            query: The search query.
            
        Returns:
            A list of search results with page numbers and snippets.
        """
        doc_data = self.get_document_content(doc_id)
        results = []
        
        for page in doc_data["pages"]:
            page_num = page["page_num"]
            text = page["text"]
            
            if query.lower() in text.lower():
                # Find the position of the query
                pos = text.lower().find(query.lower())
                
                # Get a snippet of text around the query
                start = max(0, pos - 100)
                end = min(len(text), pos + len(query) + 100)
                snippet = text[start:end]
                
                # Add to results
                results.append({
                    "page_num": page_num,
                    "snippet": snippet
                })
        
        return results
