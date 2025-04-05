# task2_generate_from_pdf.py – Generate questions from PDF content

import fitz  # PyMuPDF
from groq import Groq

def run_task_2(api_key: str):
	client = Groq(api_key=api_key)
	path = input("📄 Enter the path to your course PDF: ").strip()
	try:
		doc = fitz.open(path)
		text = "\n".join(page.get_text() for page in doc)
		doc.close()
	except Exception as e:
		print(f"❌ Error reading PDF: {e}")
		return

	prompt = (
		f"Generate 5 multiple choice questions from the content below. "
		f"Each question should include 1 correct answer and 3 distractors.\n\n{text}"
	)

	response = client.chat.completions.create(
		model="llama3-8b-8192",
		messages=[{"role": "user", "content": prompt}]
	)
	print("\n🧠 Generated Questions from PDF:\n")
	print(response.choices[0].message.content)
