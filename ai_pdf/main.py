from pdf_processor import PDFProcessor
from agent import AiResponse
from memory_semantic import SemanticMemory
from pathlib import Path

def get_pdf_path_from_input() -> Path:
	while True:
		user_input = input("📄 Enter the full path to the PDF file: ").strip().strip('"')
		pdf_path = Path(user_input)
		if not pdf_path.exists():
			print(f"❌ File not found: {pdf_path}")
		elif not pdf_path.suffix.lower() == ".pdf":
			print(f"⚠️ Not a PDF file: {pdf_path}")
		else:
			return pdf_path

def main():
	api_key = input("🔑 Enter your OpenAI API key: ")
	pdf_path = get_pdf_path_from_input()
	doc_id = pdf_path.stem

	# Step 1 – Process PDF
	processor = PDFProcessor()
	processor.process_pdf(str(pdf_path))
	full_text = processor.get_document_text(doc_id)

	# Step 2 – Build semantic memory
	memory = SemanticMemory(api_key, doc_id)
	memory.build_memory(full_text)
	memory.analyze_chunks()

	# Step 3 – AI assistant
	ai = AiResponse(api_key=api_key)
	system_prompt = (
		"You are a Socratic AI tutor. You NEVER provide final answers. "
		"You guide the user with hints, questions, and incremental steps. "
		"You respond strictly based on document content."
	)

	print("\n✅ Document processed. Ask your questions based on its content:")

	while True:
		question = input("\n❓ Ask something (or type 'exit'): ")
		if question.lower() == "exit":
			break

		chunks = memory.search(question)

		if not chunks:
			print("🤖 Sorry, that topic does not appear to be covered in the document.")
			continue

		context = "\n\n".join(chunks)
		response = ai.ask_with_context(question, context, system_prompt=system_prompt)
		print(f"\n🤖 {response}")

if __name__ == "__main__":
	main()
