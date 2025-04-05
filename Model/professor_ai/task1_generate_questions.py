# task1_generate_questions.py – Generate questions from pasted text

from groq import Groq

def run_task_1(api_key: str):
	client = Groq(api_key=api_key)

	print("\n✍️ Paste the course material below (press Enter twice to finish):")
	lines = []
	while True:
		line = input()
		if line.strip() == "":
			break
		lines.append(line)
	text = "\n".join(lines)

	prompt = (
		f"Generate 5 multiple choice questions from the material below. "
		f"Each question should have 1 correct answer and 3 distractors.\n\n{text}"
	)

	response = client.chat.completions.create(
		model="llama3-8b-8192",
		messages=[{"role": "user", "content": prompt}]
	)
	print("\n🧠 Generated Questions:\n")
	print(response.choices[0].message.content)