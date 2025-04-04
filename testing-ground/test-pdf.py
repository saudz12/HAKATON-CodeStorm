#!/usr/bin/env python3
"""
PDFProcessor Tester

A simple script to test all methods of the PDFProcessor class on a given PDF file.
"""

import os
import sys
from pdf_processor import PDFProcessor

def test_pdf_processor(pdf_path):
    """
    Test all methods of the PDFProcessor class on a given PDF file.
    
    Args:
        pdf_path: Path to the PDF file to test
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    print(f"Testing PDFProcessor with file: {pdf_path}")
    print("-" * 60)
    
    # Create a storage directory for testing
    test_dir = "pdf_test_output"
    os.makedirs(test_dir, exist_ok=True)
    
    # Initialize PDFProcessor
    processor = PDFProcessor(storage_dir=test_dir)
    
    # Test 1: process_pdf method
    print("\n1. Testing process_pdf() method:")
    try:
        doc_data = processor.process_pdf(pdf_path)
        doc_id = doc_data["metadata"]["doc_id"]
        print(f"✓ Successfully processed PDF, assigned ID: {doc_id}")
        print(f"  Title: {doc_data['metadata']['title'] or 'Not specified'}")
        print(f"  Pages: {doc_data['metadata']['page_count']}")
    except Exception as e:
        print(f"✗ Error in process_pdf(): {str(e)}")
        return
    
    # Test 2: get_document_content method
    print("\n2. Testing get_document_content() method:")
    try:
        content = processor.get_document_content(doc_id)
        print(f"✓ Successfully retrieved document content")
        print(f"  Content structure has {len(content['pages'])} pages")
    except Exception as e:
        print(f"✗ Error in get_document_content(): {str(e)}")
    
    # Test 3: get_document_text method
    print("\n3. Testing get_document_text() method:")
    try:
        text = processor.get_document_text(doc_id)
        words = len(text.split())
        chars = len(text)
        print(f"✓ Successfully extracted text")
        print(f"  Word count: {words}")
        print(f"  Character count: {chars}")
        
        # Print a sample of the text (first 150 characters)
        if text:
            sample = text[:150].replace('\n', ' ').strip()
            print(f"  Text sample: \"{sample}...\"")
    except Exception as e:
        print(f"✗ Error in get_document_text(): {str(e)}")
    
    # Test 4: list_documents method
    print("\n4. Testing list_documents() method:")
    try:
        docs = processor.list_documents()
        print(f"✓ Successfully listed documents")
        print(f"  Found {len(docs)} document(s)")
        for i, d in enumerate(docs, 1):
            print(f"  {i}. {d}")
    except Exception as e:
        print(f"✗ Error in list_documents(): {str(e)}")
    
    # Test 5: get_document_summary method
    print("\n5. Testing get_document_summary() method:")
    try:
        summary = processor.get_document_summary(doc_id)
        print(f"✓ Successfully retrieved document summary")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ Error in get_document_summary(): {str(e)}")
    
    # Test 6: search_document method
    print("\n6. Testing search_document() method:")
    
    # Try to find a common word that might be in the document
    common_words = ["the", "and", "is", "in", "to", "of", "for"]
    
    for word in common_words:
        try:
            results = processor.search_document(doc_id, word)
            if results:
                print(f"✓ Successfully searched for '{word}'")
                print(f"  Found {len(results)} occurrence(s)")
                
                # Show a snippet from the first result
                if results:
                    page = results[0]["page_num"]
                    snippet = results[0]["snippet"].replace('\n', ' ').strip()
                    if len(snippet) > 100:
                        snippet = snippet[:100] + "..."
                    print(f"  First occurrence (Page {page}): \"{snippet}\"")
                break
            else:
                print(f"  No occurrences of '{word}' found, trying another word...")
        except Exception as e:
            print(f"✗ Error in search_document(): {str(e)}")
            break
    else:
        print("  Could not find any common words in the document.")
    
    print("\nAll tests completed!")
    
    return doc_id

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_processor_tester.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_pdf_processor(pdf_path)