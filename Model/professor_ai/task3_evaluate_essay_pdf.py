# task3_evaluate_essay_pdf.py – Evaluate student essay from a PDF

import fitz
from groq import Groq

def run_task_3(api_key: str):
	client = Groq(api_key=api_key)
	path = input("📄 Enter the path to the student's essay PDF: ").strip()
	try:
		doc = fitz.open(path)
		text = "\n".join(page.get_text() for page in doc)
		doc.close()
	except Exception as e:
		print(f"❌ Error reading PDF: {e}")
		return

	prompt = (
		"Evaluate the following student essay. Analyze content, structure, grammar, and coherence. "
		"Then give a score from 1 to 10 and a summary of improvements.\n\n"
		f"Essay:\n{text}"
	)

	response = client.chat.completions.create(
		model="llama3-8b-8192",
		messages=[{"role": "user", "content": prompt}]
	)
	print("\n📝 Essay Evaluation:\n")
	print(response.choices[0].message.content)
