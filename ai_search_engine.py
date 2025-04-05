# ai_web_search_assistant/main.py – single-language source (ro/en) version

import os
from openai import OpenAI
from serpapi import GoogleSearch
import langdetect

# CONFIG
OPENAI_API_KEY = input("🔑 Enter your OpenAI API key: ") 
SERP_API_KEY = input("🔑 Enter your SerpAPI key: ")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_user_preferences():
	print("\n🔧 Set your search preferences:")
	print("1. Domain: [1] Math [2] CS [3] Physics [4] Biology [5] Custom")
	domain_choice = input("Enter choice: ").strip()
	if domain_choice == "5":
		domain = input("Enter custom domain: ").strip()
	else:
		domains = {
			"1": "matematică",
			"2": "informatică",
			"3": "fizică",
			"4": "biologie"
		}
		domain = domains.get(domain_choice, "general")

	print("2. Level: [1] High School [2] University")
	level_choice = input("Enter level: ").strip()
	levels = {
		"1": "liceu",
		"2": "universitate"
	}
	level = levels.get(level_choice, "elev")

	print("3. Resource Type: [1] General Web [2] Academic [3] Videos")
	source_choice = input("Enter resource type: ").strip()
	sources = {
		"1": "general",
		"2": "scholar",
		"3": "youtube.com"
	}
	source = sources.get(source_choice, "general")

	return domain, level, source

def build_query(question: str, domain: str, level: str, source: str, lang: str = "en") -> str:
	lang_filter = " site:.ro" if lang == "ro" else ""
	if source == "youtube.com":
		return f"{question} {domain} site:youtube.com{lang_filter}"
	elif source == "scholar":
		return f"{question} {domain} {level}{lang_filter}"
	else:
		return f"{question} {domain} {level}{lang_filter}"

def search_web(query: str, mode: str = "general") -> str:
	print(f"\n🌐 Searching the web for: {query} [mode: {mode}]\n")
	params = {
		"q": query,
		"api_key": SERP_API_KEY,
		"num": 3,
		"engine": "google_scholar" if mode == "scholar" else "google"
	}
	search = GoogleSearch(params)
	results = search.get_dict()

	output = []
	for r in results.get("organic_results", [])[:3]:
		title = r.get("title", "Fără titlu")
		link = r.get("link", "Fără link")
		snippet = r.get("snippet", "")
		output.append(f"{title}\n{link}\n{snippet}\n")

	return "\n".join(output)

def detect_language(text: str) -> str:
	try:
		lang = langdetect.detect(text)
		return lang
	except:
		return "ro"  # fallback în română dacă nu e detectabil

def ask_ai(question: str, context: str, domain: str, level: str, source: str, lang: str) -> str:
	if lang == "ro":
		intro = (
			f"Ești un asistent educațional care ajută un elev de nivel {level} interesat de domeniul {domain}.")
		guidance = (
			" Ai acces la o sursă în limba română. Oferă o explicație clară, apoi formulează întrebări care să ghideze elevul. "
			"Include un link către sursa utilizată."
		)
	else:
		intro = (
			f"You are an educational AI assistant helping a {level} student interested in {domain}.")
		guidance = (
			" You have access to one online source. Provide a short, clear explanation, followed by guiding questions. "
			"Include a relevant source link."
		)

	prompt = (
		f"{intro}\n{guidance}\n\n"
		f"Search Result:\n{context}\n\n"
		f"Student Question: {question}\n\n"
		"Generate the answer based on the single-language source above."
	)

	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": "You are a helpful AI tutor."},
			{"role": "user", "content": prompt}
		]
	)
	return response.choices[0].message.content

def main():
	domain, level, source_type = get_user_preferences()

	while True:
		question = input("\n❓ Ask your educational question (or type 'exit'): ")
		if question.lower() == "exit":
			break

		lang = detect_language(question)
		query = build_query(question, domain, level, source_type, lang=lang)
		results = search_web(query, mode=source_type if source_type == "scholar" else "general")

		ai_reply = ask_ai(question, results, domain, level, source_type, lang)
		print(f"\n🤖 AI Response:\n{ai_reply}")

if __name__ == "__main__":
	main()