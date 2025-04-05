# task4_custom_material.py – Generate personalized learning material

from groq import Groq

def run_task_4(api_key: str):
	client = Groq(api_key=api_key)
	topic = input("📚 Enter the topic (e.g. derivatives, Python loops): ").strip()
	level = input("🎓 Student level [beginner/intermediate/advanced]: ").strip()

	prompt = (
		f"Create a personalized learning resource on the topic: {topic}. "
		f"Target level: {level}. The output should include a short explanation, 2 examples, and 3 practice questions."
	)

	response = client.chat.completions.create(
		model="llama3-8b-8192",
		messages=[{"role": "user", "content": prompt}]
	)
	print("\n🎯 Personalized Material:\n")
	print(response.choices[0].message.content)
