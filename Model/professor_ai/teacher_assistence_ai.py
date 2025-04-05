import os
from task1_generate_questions import run_task_1
from task2_generate_from_pdf import run_task_2
from task3_evaluate_essay_pdf import run_task_3
from task4_custom_material import run_task_4

def main():
	api_key = input("Enter your Groq API key: ").strip()

	while True:
		print("\nAI Assistant for Teachers: Choose a task")
		print("1. Generate test questions from pasted text")
		print("2. Generate test questions from PDF")
		print("3. Evaluate student essay from PDF")
		print("4. Generate personalized material")
		print("0. Exit")
		choice = input("Enter choice: ").strip()

		if choice == "1":
			run_task_1(api_key)
		elif choice == "2":
			run_task_2(api_key)
		elif choice == "3":
			run_task_3(api_key)
		elif choice == "4":
			run_task_4(api_key)
		elif choice == "0":
			print("Exiting. Have a great day!")
			break
		else:
			print("Invalid option.")

if __name__ == "__main__":
	main()
